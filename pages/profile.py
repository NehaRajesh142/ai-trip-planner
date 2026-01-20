import streamlit as st
from firebase_config import db

st.title("👤 My Profile")

# Must be logged in
if "user" not in st.session_state or not st.session_state.user:
    st.error("Please log in first")
    st.switch_page("pages/login.py")

email = st.session_state.user

# Fetch user doc from Firestore
users_ref = db.collection("users").where("email", "==", email).stream()

user_doc = None
user_data = {}

for doc in users_ref:
    user_doc = doc
    user_data = doc.to_dict()
    break

if not user_doc:
    st.error("Profile not found in database")
    st.stop()

# -------- PROFILE FORM --------
st.subheader("Edit your details")

name = st.text_input("Full Name", value=user_data.get("name", ""))
phone = st.text_input("Phone Number", value=user_data.get("phone", ""))

travel_style = st.selectbox(
    "Preferred Travel Style",
    ["Adventure", "Luxury", "Budget", "Cultural", "Relaxed"],
    index=["Adventure","Luxury","Budget","Cultural","Relaxed"]
        .index(user_data.get("travel_style", "Adventure"))
)

budget = st.select_slider(
    "Typical Trip Budget",
    options=["Low", "Medium", "High", "Premium"],
    value=user_data.get("budget", "Medium")
)

if st.button("💾 Save Profile"):
    db.collection("users").document(user_doc.id).update({
        "name": name,
        "phone": phone,
        "travel_style": travel_style,
        "budget": budget
    })

    st.success("Profile updated successfully!")

st.markdown("---")
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")
