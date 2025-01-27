import pandas as pd
import streamlit as st
from core import methods as m1
from config import pdict
from src.infrastrucure.repositories.feedback_repository import FeedbackRepository
from src.infrastrucure.repositories.user_repository import UserRepository
from src.infrastrucure.repositories.malfunction_repository import MalfunctionRepository

# Initialize repositories
user_repo = UserRepository()
feedback_repo = FeedbackRepository()
malfunction_repo = MalfunctionRepository()

# Add a test user if not already present
if not any(user['email'] == 'test@example.com' for user in user_repo.users):
    user_repo.save({'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'})

# Session state for user login
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None


def load_data():
    """Load and preprocess all required data."""
    df_postal_codes = pd.read_csv("datasets/" + pdict["file_geodat_plz"], delimiter=";")
    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
    df_preprocessed_stations = m1.preprop_lstat(df_location_stations, df_postal_codes, pdict)
    gdf_station_occurrences_by_plz = m1.count_plz_occurrences(df_preprocessed_stations)
    df_resident_data = pd.read_csv("datasets/" + pdict["file_residents"], delimiter=",")
    gdf_preprocessed_residents = m1.preprop_resid(df_resident_data, df_postal_codes, pdict)
    return gdf_station_occurrences_by_plz, gdf_preprocessed_residents


def login_page():
    """Render the login page."""
    st.title("Login", anchor="login-title")
    st.markdown("<h3 style='color: #6c757d;'>Please log in to access the platform</h3>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login", key="login_button", help="Click to login"):
        user = user_repo.get_by_email_and_password(email, password)
        if user:
            st.session_state.logged_in_user = user
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid credentials. Please try again.")


def feedback_history():
    """Render the feedback history for logged-in users."""
    st.subheader("Feedback History", anchor="feedback-history")
    user_id = st.session_state.logged_in_user['id']
    feedbacks = feedback_repo.get_by_user_id(user_id)

    if feedbacks:
        # Count the feedbacks for badges
        feedback_count = len(feedbacks)
        badge_label = ""

        if feedback_count >= 4:
            badge_label = "Gold Contributor"
        elif feedback_count == 3:
            badge_label = "Silver Contributor"
        elif feedback_count == 2:
            badge_label = "Bronze Contributor"
        elif feedback_count == 1:
            badge_label = "New Contributor"

        # Display badge label
        if badge_label:
            st.markdown(f"<h3 style='color: #28a745;'>🏅 {badge_label}</h3>", unsafe_allow_html=True)

        for fb in feedbacks:
            with st.container():
                st.markdown(f"### Charging Station: {fb['station_name']}")
                st.markdown(f"**Feedback:** {fb['feedback_text']}")
                st.progress(int((fb['rating'] / 5) * 100))  # Progress bar based on feedback rating
                st.write("---")
    else:
        st.write("No feedback found. Please submit feedback.")


def submit_feedback():
    """Allow users to submit new feedback."""
    st.subheader("Submit Feedback", anchor="submit-feedback")

    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
    df_location_stations["Unique_Label"] = df_location_stations["Betreiber"] + " - " + df_location_stations[
        "Straße"] + " " + df_location_stations["Hausnummer"].fillna("")

    unique_station_labels = df_location_stations["Unique_Label"].unique()

    # Let the user select a station
    selected_station = st.selectbox("Select Charging Station", unique_station_labels, key="station_select")

    # Get the logged-in user's ID
    user_id = st.session_state.logged_in_user['id']

    # Get the feedback text and rating
    feedback_text = st.text_area("Suggestions", placeholder="Your feedback...")
    rating = st.slider("Feedback Rating", min_value=1, max_value=5)

    if st.button("Submit Feedback", key="submit_feedback_btn"):
        if feedback_text.strip():
            feedback = {
                'user_id': user_id,
                'feedback_text': feedback_text,
                'rating': rating,
                'station_name': selected_station,
                'status': "Submitted"
            }
            feedback_repo.save(feedback)
            st.success("Feedback submitted successfully!")
        else:
            st.warning("Please provide feedback text.")


def sidebar_malfunctions():
    """Display malfunctions in the sidebar and let the user select what to view."""
    st.sidebar.title("Malfunction Management")

    # Sidebar options to view all malfunctions
    show_all = st.sidebar.button("Show All Malfunctions")

    if show_all:
        show_all_malfunctions()


def show_all_malfunctions():
    """Render the malfunction report history for logged-in users."""
    st.subheader("Malfunction Report History", anchor="malfunction-history")

    malfunctions = malfunction_repo.get_all_malfunctions()

    if malfunctions:
        for malfunction in malfunctions:
            with st.container():
                st.markdown(f"### Station: {malfunction['station_id']}")
                st.markdown(f"**Description:** {malfunction['description']}")
                st.markdown(f"**Severity:** {malfunction['severity']}")
                st.markdown(f"**Status:** {malfunction['status']}")
                st.markdown(f"**Reported At:** {malfunction['timestamp']}")
                st.write("---")
    else:
        st.write("No malfunctions reported.")

def report_malfunction():
    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
    df_location_stations["Unique_Label"] = df_location_stations["Betreiber"] + " - " + df_location_stations[
        "Straße"] + " " + df_location_stations["Hausnummer"].fillna("")

    unique_station_labels = df_location_stations["Unique_Label"].unique()

    st.subheader("Report Malfunction", anchor="report-malfunction")

    # Let the user select a station
    selected_station = st.selectbox("Select Charging Station", unique_station_labels, key="station_select")

    user_id = st.session_state.logged_in_user['id']

    malfunction_description = st.text_area("Describe the Issue", placeholder="What is the problem?")
    severity = st.slider("Severity Level", min_value=1, max_value=5, help="1 = Minor, 5 = Critical")

    if st.button("Submit Malfunction", key="submit_malfunction_btn"):
        if malfunction_description.strip():
            malfunction_report = {
                'user_id': user_id,
                'station_id': selected_station,
                'description': malfunction_description,
                'timestamp': pd.Timestamp.now().isoformat(),
                'severity': severity,
                'status': "Reported"
            }
            malfunction_repo.save(malfunction_report)  # Save the report
            st.success("Malfunction reported successfully!")
        else:
            st.warning("Please describe the malfunction.")


def malfunction_history():
    """Render the malfunction report history for logged-in users."""
    st.subheader("Malfunction Report History", anchor="malfunction-history")
    user_id = st.session_state.logged_in_user['id']
    malfunctions = malfunction_repo.get_by_user_id(user_id)

    if malfunctions:
        for malfunction in malfunctions:
            with st.container():
                st.markdown(f"### Station: {malfunction['station_id']}")
                st.markdown(f"**Description:** {malfunction['description']}")
                st.markdown(f"**Severity:** {malfunction['severity']}")
                st.markdown(f"**Status:** {malfunction['status']}")
                st.markdown(f"**Reported At:** {malfunction['timestamp']}")
                st.write("---")
    else:
        st.write("No malfunctions reported.")


def view_profile():
    """Render the 'View Profile' section with feedback and malfunction history."""
    st.title("View Profile", anchor="profile-title")
    menu = st.radio("Options", ["Feedback History", "Submit Feedback", "View Malfunction History"], key="profile_menu")

    if menu == "Feedback History":
        feedback_history()
    elif menu == "Submit Feedback":
        submit_feedback()
    elif menu == "View Malfunction History":
        malfunction_history()



def main_app():
    gdf_station_occurrences_by_plz, gdf_preprocessed_residents = load_data()
    m1.make_streamlit_electric_Charging_resid(gdf_station_occurrences_by_plz, gdf_preprocessed_residents)


def main():
    if st.session_state.logged_in_user:
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Select Page", ["Main App", "View Profile", "Report Malfunction", "Logout", "Show All Malfunctions"])

        if menu == "Main App":
            main_app()
        elif menu == "View Profile":
            view_profile()
        elif menu == "Report Malfunction":
            report_malfunction()
        elif menu == "Show All Malfunctions":  # Corrected label
            show_all_malfunctions()
        elif menu == "Logout":
            st.session_state.logged_in_user = None
            st.success("You have been logged out.")
    else:
        login_page()


if __name__ == "__main__":
    main()
