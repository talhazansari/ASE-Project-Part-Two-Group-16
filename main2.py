import streamlit as st

from feedback.application.services.FeedbackService import FeedbackService
from feedback.application.services.UserService import UserService
from feedback.domain.entties.user import User
from feedback.domain.value_objects.feedback_details import FeedbackDetails
from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository
from feedback.infrastructure.repositories.user_repository import UserRepository
from session import Session

# Initialize repositories
user_repository = UserRepository()
feedback_repository = FeedbackRepository()

# Initialize services
user_service = UserService(user_repository)
feedback_service = FeedbackService(feedback_repository, user_repository)

# Initialize session
session = Session()

# Add a user for testing
user_repository.save(User(user_id="1", name="John Doe", email="johndoe@example.com", password="password123"))


# User login page
def login_page():
    st.title("Login to Your Profile")

    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")

    if st.button("Login"):
        user = user_service.login(email, password)
        if user:
            session.login(user)  # Log in the user and set the session
            st.success(f"Welcome, {user.name}!")
            show_dashboard()  # Navigate to the dashboard after successful login
        else:
            st.error("Invalid credentials!")


# Dashboard page to submit feedback and view history
def show_dashboard():
    st.title(f"{session.get_logged_in_user().name}'s Dashboard")

    # Show the feedback form
    feedback_form()

    # Logout button
    if st.button("Logout"):
        session.logout()  # Log out the user and clear the session
        st.success("You have been logged out.")
        main()  # After logout, go back to the login page


def feedback_form():
    st.subheader("Submit Your Feedback")

    feedback_text = st.text_area("Feedback Text", "")
    rating = st.slider("Rating", min_value=1, max_value=5, value=3)

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            feedback_details = FeedbackDetails(feedback_text, rating)
            feedback = feedback_service.submit_feedback(session.get_logged_in_user().id, feedback_details)
            st.success("Feedback submitted successfully!")
            show_feedback_history()
        else:
            st.warning("Please enter feedback text.")


def show_feedback_history():
    st.subheader("Your Feedback History")

    user_profile = session.get_logged_in_user().get_profile()

    if user_profile.feedback_history:
        for feedback in user_profile.feedback_history:
            st.write(f"Feedback: {feedback.feedback_details.feedback_text}")
            st.write(f"Rating: {feedback.feedback_details.rating}")
            st.write(f"Status: {feedback.status}")
            st.write("---")
    else:
        st.write("You have no feedback history.")


# Main app flow
def main():
    if session.get_logged_in_user():
        show_dashboard()  # Show dashboard if user is logged in
    else:
        login_page()  # Show login page if no user is logged in


if __name__ == "__main__":
    main()
