import streamlit as st

from feedback.application.services.FeedbackService import FeedbackService
from feedback.application.services.UserService import UserService
from feedback.domain.entties.user import User
from feedback.domain.value_objects.feedback_details import FeedbackDetails
from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository
# from feedback.infrastructure.repositories.user_repository import UserRepository
from session import Session

# Initialize repositories
# user_repository = UserRepository()
# feedback_repository = FeedbackRepository()

# # Initialize services
# user_service = UserService(user_repository)
# feedback_service = FeedbackService(feedback_repository, user_repository)

# # Initialize session
# session = Session()

# # Add a user for testing
# user_repository.save(User(user_id="1", name="John Doe", email="a@a.com", password="1"))


# # User login page
# def login_page():
#     st.title("Login to Your Profile")

#     email = st.text_input("Email", "")
#     password = st.text_input("Password", "", type="password")

#     if st.button("Login"):
#         user = user_service.login(email, password)
#         if user:
#             session.login(user)  # Log in the user and set the session
#             st.success(f"Welcome, {user.name}!")
#             show_dashboard()  # Navigate to the dashboard after successful login
#         else:
#             st.error("Invalid credentials!")


# # Dashboard page to submit feedback and view history
# def show_dashboard():
#     st.title(f"{session.get_logged_in_user().name}'s Dashboard")

#     # Show the feedback form
    
#     feedback_form()

#     # Logout button
#     if st.button("Logout"):
#         session.logout()  # Log out the user and clear the session
#         st.success("You have been logged out.")
#         main()  # After logout, go back to the login page


# def feedback_form():
#     st.subheader("Submit Your Feedback")

#     feedback_text = st.text_area("Feedback Text", "")
#     rating = st.slider("Rating", min_value=1, max_value=5, value=3)

#     if st.button("Submit Feedback"):
#         if feedback_text.strip():
#             feedback_details = FeedbackDetails(feedback_text, rating)
#             feedback = feedback_service.submit_feedback(session.get_logged_in_user().id, feedback_details)
#             st.success("Feedback submitted successfully!")
#             show_feedback_history()
#         else:
#             st.warning("Please enter feedback text.")


# def show_feedback_history():
#     st.write("inside the feedback history ,,,,,,")
#     st.button("Your Feedback History")

#     user_profile = session.get_logged_in_user().get_profile()

#     if user_profile.feedback_history:
#         for feedback in user_profile.feedback_history:
#             st.write(f"Feedback: {feedback.feedback_details.feedback_text}")
#             st.write(f"Rating: {feedback.feedback_details.rating}")
#             st.write(f"Status: {feedback.status}")
#             st.write("---")
#     else:
#         st.write("You have no feedback history.")


# # Main app flow
# def main():
#     if session.get_logged_in_user():
#         # show_feedback_history()
#         show_dashboard()  # Show dashboard if user is logged in
        
#     else:
#         login_page()  # Show login page if no user is logged in


# if __name__ == "__main__":
#     main()

 ## save in here in file
# import streamlit as st

# # Initialize session state for user data if not already set
# if "logged_in_user" not in st.session_state:
#     st.session_state.logged_in_user = None

# if "feedback_history" not in st.session_state:
#     st.session_state.feedback_history = []

# # Mock user repository
# USERS = {"johndoe@example.com": {"password": "password123", "name": "John Doe"},"ali@a.com": {"password": "1", "name": "ali"}}


# # Login function
# def login(email, password):
#     user = USERS.get(email)
#     if user and user["password"] == password:
#         return {"email": email, "name": user["name"]}
#     return None


# # Feedback submission
# def submit_feedback(user_email, feedback_text, rating):
#     st.session_state.feedback_history.append({
#         "email": user_email,
#         "feedback_text": feedback_text,
#         "rating": rating,
#     })


# # Login page
# def login_page():
#     st.title("Login to Your Profile")

#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = login(email, password)
#         if user:
#             st.session_state.logged_in_user = user  # Save user in session state
#             st.success(f"Welcome, {user['name']}!")
#         else:
#             st.error("Invalid credentials!")


# # Dashboard page
# def show_dashboard():
#     st.title(f"{st.session_state.logged_in_user['name']}'s Dashboard")

#     feedback_text = st.text_area("Feedback Text", "")
#     rating = st.slider("Rating", min_value=1, max_value=5, value=3)

#     if st.button("Submit Feedback"):
#         if feedback_text.strip():
#             submit_feedback(st.session_state.logged_in_user["email"], feedback_text, rating)
#             st.success("Feedback submitted successfully!")
#         else:
#             st.warning("Please enter feedback text.")

#     st.subheader("Your Feedback History")
#     user_feedback = [f for f in st.session_state.feedback_history if f["email"] == st.session_state.logged_in_user["email"]]

#     if user_feedback:
#         for feedback in user_feedback:
#             st.write(f"Feedback: {feedback['feedback_text']}")
#             st.write(f"Rating: {feedback['rating']}")
#             st.write("---")
#     else:
#         st.write("No feedback history available.")

#     if st.button("Logout"):
#         st.session_state.logged_in_user = None
#         st.success("You have been logged out.")


# # Main app flow
# def main():
#     if st.session_state.logged_in_user:
#         show_dashboard()
#     else:
#         login_page()


# if __name__ == "__main__":
#     main()


# import streamlit as st
# from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository
# from feedback.infrastructure.repositories.user_repository import FeedbackRepository

# # Initialize repository
# feedback_repo = FeedbackRepository()

# def feedback_form():
#     st.title("Submit Feedback")

#     user_id = st.text_input("User ID")
#     feedback_text = st.text_area("Feedback")
#     rating = st.slider("Rating", min_value=1, max_value=5)

#     if st.button("Submit Feedback"):
#         if user_id and feedback_text.strip():
#             feedback = {
#                 'user_id': user_id,
#                 'feedback_text': feedback_text,
#                 'rating': rating,
#                 'status': "Submitted"
#             }
#             feedback_repo.save(feedback)
#             st.success("Feedback submitted successfully!")
#         else:
#             st.warning("Please provide User ID and Feedback.")

# def show_feedback_history():
#     st.title("Feedback History")

#     user_id = st.text_input("Enter User ID to view history")
#     if st.button("View History"):
#         feedbacks = feedback_repo.get_by_user_id(user_id)
#         if feedbacks:
#             for fb in feedbacks:
#                 st.write(f"Feedback: {fb['feedback_text']}")
#                 st.write(f"Rating: {fb['rating']}")
#                 st.write(f"Status: {fb['status']}")
#                 st.write("---")
#         else:
#             st.write("No feedback found for this User ID.")

# def main():
#     st.sidebar.title("Menu")
#     menu = st.sidebar.radio("Select Page", ["Submit Feedback", "View Feedback History"])

#     if menu == "Submit Feedback":
#         feedback_form()
#     elif menu == "View Feedback History":
#         show_feedback_history()

# if __name__ == "__main__":
#     main()

import streamlit as st
from feedback.infrastructure.repositories.user_repository import UserRepository
from feedback.infrastructure.repositories.feedback_repository import FeedbackRepository

# Initialize repositories
user_repo = UserRepository()
feedback_repo = FeedbackRepository()

# Add a test user
if not any(user['email'] == 'test@example.com' for user in user_repo.users):
    user_repo.save({'id': '1', 'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'})

# Session state for user login
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None


def login_page():
    """Render the login page."""
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = user_repo.get_by_email_and_password(email, password)
        if user:
            st.session_state.logged_in_user = user  # Set the logged-in user in session state
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid credentials. Please try again.")


def feedback_form():
    """Render the feedback form for logged-in users."""
    st.title("Submit Feedback")

    user_id = st.session_state.logged_in_user['id']
    feedback_text = st.text_area("Feedback")
    rating = st.slider("Rating", min_value=1, max_value=5)

    if st.button("Submit Feedback"):
        if feedback_text.strip():
            feedback = {
                'user_id': user_id,
                'feedback_text': feedback_text,
                'rating': rating,
                'status': "Submitted"
            }
            feedback_repo.save(feedback)
            st.success("Feedback submitted successfully!")
        else:
            st.warning("Please provide feedback text.")


def show_feedback_history():
    """Render feedback history for logged-in users."""
    st.title("Feedback History")

    user_id = st.session_state.logged_in_user['id']
    feedbacks = feedback_repo.get_by_user_id(user_id)

    if feedbacks:
        for fb in feedbacks:
            st.write(f"Feedback: {fb['feedback_text']}")
            st.write(f"Rating: {fb['rating']}")
            st.write(f"Status: {fb['status']}")
            st.write("---")
    else:
        st.write("No feedback found.")


def main():
    if st.session_state.logged_in_user:
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Select Page", ["Submit Feedback", "View Feedback History", "Logout"])

        if menu == "Submit Feedback":
            feedback_form()
        elif menu == "View Feedback History":
            show_feedback_history()
        elif menu == "Logout":
            st.session_state.logged_in_user = None
            st.success("You have been logged out.")
    else:
        login_page()


if __name__ == "__main__":
    main()


