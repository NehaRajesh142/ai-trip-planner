import streamlit as st

st.title("Dashboard")

if "logged_in" not in st.session_state:
    st.switch_page("login.py")

st.write("Welcome to your AI Trip Planner!")

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("login.py")
