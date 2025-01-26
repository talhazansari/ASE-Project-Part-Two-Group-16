import pandas as pd
import streamlit as st
from core import methods as m1
from config import pdict
from src.infrastrucure.repositories.feedback_repository import FeedbackRepository
from src.infrastrucure.repositories.user_repository import UserRepository

# Initialize repositories
user_repo = UserRepository()
feedback_repo = FeedbackRepository()

# Add a test user
if not any(user['email'] == 'test@example.com' for user in user_repo.users):
    user_repo.save({'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'})

# Session state for user login
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

def load_data():
    """Load and preprocess all required data."""
    # Load geographic data for postal codes
    df_postal_codes = pd.read_csv("datasets/" + pdict["file_geodat_plz"], delimiter=";")

    # Load and preprocess location station data
    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
    df_preprocessed_stations = m1.preprop_lstat(df_location_stations, df_postal_codes, pdict)
    gdf_station_occurrences_by_plz = m1.count_plz_occurrences(df_preprocessed_stations)

    # Load and preprocess resident data
    df_resident_data = pd.read_csv("datasets/" + pdict["file_residents"], delimiter=",")
    gdf_preprocessed_residents = m1.preprop_resid(df_resident_data, df_postal_codes, pdict)

    return gdf_station_occurrences_by_plz, gdf_preprocessed_residents

def login_page():
    """Render the login page."""
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = user_repo.get_by_email_and_password(email, password)
        if user:
            st.session_state.logged_in_user = user
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid credentials. Please try again.")

def feedback_history():
    """Render the feedback history for logged-in users."""
    st.subheader("Feedback History")

    user_id = st.session_state.logged_in_user['id']
    feedbacks = feedback_repo.get_by_user_id(user_id)

    if feedbacks:
        for fb in feedbacks:
            # Display station name and feedback text
            st.write(f"Charging Station: {fb['station_name']}")  # Show the station name
            st.write(f"Feedback: {fb['feedback_text']}")
            st.progress(int((fb['rating'] / 5) * 100))  # Progress bar based on feedback rating
            st.write("---")
    else:
        st.write("No feedback found. Please submit feedback.")
def submit_feedback():
    """Allow users to submit new feedback."""
    st.subheader("Submit Feedback")

    df_location_stations = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")

    # Create unique label (station name + address)
    df_location_stations["Unique_Label"] = df_location_stations["Betreiber"] + " - " + df_location_stations[
        "Straße"] + " " + df_location_stations["Hausnummer"].fillna("")

    unique_station_labels = df_location_stations["Unique_Label"].unique()

    # Let the user select a station
    selected_station = st.selectbox("Select Charging Station", unique_station_labels)

    # Get the logged-in user's ID
    user_id = st.session_state.logged_in_user['id']

    # Get the feedback text and rating
    feedback_text = st.text_area("Suggestions")
    rating = st.slider("Feedback", min_value=1, max_value=5)

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            # Store both station name and feedback text
            feedback = {
                'user_id': user_id,
                'feedback_text': feedback_text,  # Store user input feedback text
                'rating': rating,
                'station_name': selected_station,  # Save station name as well
                'status': "Submitted"
            }
            feedback_repo.save(feedback)
            st.success("Feedback submitted successfully!")
        else:
            st.warning("Please provide feedback text.")

def view_profile():
    """Render the 'View Profile' section with feedback history and submission."""
    st.title("View Profile")

    menu = st.radio("Options", ["Feedback History", "Submit Feedback"])

    if menu == "Feedback History":
        feedback_history()
    elif menu == "Submit Feedback":
        submit_feedback()

def main_app():
    gdf_station_occurrences_by_plz, gdf_preprocessed_residents = load_data()
    m1.make_streamlit_electric_Charging_resid(
        gdf_station_occurrences_by_plz, gdf_preprocessed_residents
    )

def main():
    if st.session_state.logged_in_user:
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Select Page", ["Main App", "View Profile", "Logout"])

        if menu == "Main App":
            main_app()
        elif menu == "View Profile":
            view_profile()
        elif menu == "Logout":
            st.session_state.logged_in_user = None
            st.success("You have been logged out.")
    else:
        login_page()

if __name__ == "__main__":
    main()
