import streamlit as st
from firebase_config import db

st.title("Create Account")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if not email or not password:
        st.error("Fill all fields")
    else:
        users_ref = db.collection("users")

        # check if already exists
        existing = users_ref.where("email", "==", email).stream()
        if any(True for _ in existing):
            st.warning("Account already exists. Go to Login.")
            st.switch_page("login.py")
        else:
            users_ref.add({
                "email": email,
                "password": password
            })
            st.success("Account created! Please log in.")
            st.switch_page("pages/login.py")
