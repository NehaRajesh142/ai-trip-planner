import streamlit as st
from firebase_config import db

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not email or not password:
        st.error("Please enter both email and password")
    else:
        users = db.collection("users").where("email", "==", email).stream()

        found = False

        for user in users:
            data = user.to_dict()

            if data.get("password") == password:
                found = True
                st.session_state.user = email
                st.session_state.logged_in = True

                st.success("Logged in successfully!")

                # ✅ Correct navigation to main app
                st.switch_page("app.py")

        if not found:
            st.error("Invalid credentials or no account found")

st.write("New user?")

if st.button("Go to Sign Up"):
    st.switch_page("pages/signup.py")   # <-- THIS WAS YOUR BUG
