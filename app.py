import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time
from gemini_ai import generate_itinerary

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Trip Planner", layout="wide")

# ---------------- LOGIN GATE ----------------
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

# ---------------- LOGOUT / PROFILE BAR ----------------
colA, colB, colC = st.columns([5, 1, 1])

with colA:
    st.success(f"Logged in as: {st.session_state.user}")

with colB:
    if st.button("👤 Profile"):
        st.switch_page("pages/profile.py")

with colC:
    if st.button("Logout 🚪"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# ---------------- DEFAULT STATE ----------------
if "selected_service" not in st.session_state:
    st.session_state.selected_service = "Holidays"

if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "places" not in st.session_state:
    st.session_state.places = []

# ---------------- STYLES ----------------
st.markdown("""
<style>
.tile-btn button {
    background: linear-gradient(90deg, #FF5722, #FF9800);
    color: white;
    font-weight: 600;
    border-radius: 14px;
    height: 90px;
    width: 100%;
    border: none;
    transition: all 0.3s ease;
}
.tile-btn button:hover {
    transform: scale(1.08);
    background: linear-gradient(90deg, #FF9800, #FF5722);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h2 style='text-align:center; color:#FF5722;'>✈️ AI Trip Planner</h2>", unsafe_allow_html=True)

# ---------------- SERVICE TILES ----------------
services = [
    "Hotels", "Flights", "Trains", "Cabs",
    "Villas & Apts", "Bus", "Activities",
    "Couple Hotels", "Holidays", "Metro",
    "Meals & Deals", "Airport Cabs"
]

cols = st.columns(6)
for i, service in enumerate(services):
    with cols[i % 6]:
        st.markdown('<div class="tile-btn">', unsafe_allow_html=True)
        if st.button(service, key=service):
            st.session_state.selected_service = service
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SEARCH PANEL ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color:#FF5722;'>🔍 {st.session_state.selected_service} Planner</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    destination = st.text_input("Destination*", placeholder="e.g. Paris, Goa, Tokyo")
    start = st.date_input("Start Date")
    end = st.date_input("End Date")

with col2:
    people = st.number_input("Guests / Seats", min_value=1, max_value=10, value=1)
    generate = st.button("✨ Generate AI Plan", use_container_width=True)

# ---------------- HELPER: SAFE AI RESPONSE PARSER ----------------
def parse_ai_response(response):
    # If Gemini returns structured data
    if isinstance(response, dict):
        return response.get("places", []), response.get("itinerary", "")

    # If Gemini returns plain text
    return [], str(response)

# ---------------- GENERATE AI ITINERARY ----------------
if generate:
    if destination.strip() == "":
        st.error("Please enter a destination")
    elif start > end:
        st.error("End date must be after start date")
    else:
        with st.spinner("🧠 Gemini AI is planning your trip..."):
            raw_plan = generate_itinerary(
                destination,
                (end - start).days + 1,
                "moderate",
                st.session_state.selected_service,
                st.session_state.user
            )

        st.session_state.places, st.session_state.itinerary = parse_ai_response(raw_plan)

# ---------------- DISPLAY MAP & ITINERARY ----------------
if st.session_state.itinerary:

    # ---- MAP ----
    st.markdown("## 🗺️ Places You’ll Visit")

    geolocator = Nominatim(user_agent="ai_trip_planner")

    try:
        city_loc = geolocator.geocode(destination)
        center_lat, center_lon = city_loc.latitude, city_loc.longitude
    except:
        center_lat, center_lon = 0, 0

    travel_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    for place in st.session_state.places:
        try:
            time.sleep(1)
            loc = geolocator.geocode(f"{place['name']}, {destination}")
            if loc:
                folium.Marker(
                    location=[loc.latitude, loc.longitude],
                    popup=f"<b>{place['name']}</b><br>{place.get('description','')}",
                    tooltip=place['name'],
                    icon=folium.Icon(color="orange", icon="map-marker")
                ).add_to(travel_map)
        except:
            pass

    st_folium(travel_map, width=1100, height=500)

    # ---- ITINERARY ----
    st.markdown("## ✨ Your AI-Generated Trip Plan")

    formatted_itinerary = ""
    for line in str(st.session_state.itinerary).split("\n"):
        if line.strip().lower().startswith("day"):
            formatted_itinerary += f"### {line.strip()}\n"
        elif line.strip():
            formatted_itinerary += f"- {line.strip()}\n"

    st.markdown(formatted_itinerary)

# ---------------- DEALS ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#4CAF50;'>🌟 Today's Deals</h4>", unsafe_allow_html=True)

for d in [
    "🔥 50% off on Hotels (Special Deals)",
    "✈️ 20% Cashback on Flights",
    "🍔 Extra 10% off on Meals & Deals",
    "🚖 Flat 15% off on Airport Cabs",
    "🏝️ Up to 30% off on Holidays Packages",
    "🎟️ Buy 1 Get 1 Free on Activities"
]:
    st.success(d)
