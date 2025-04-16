import streamlit as st
import json
from PIL import Image
import os

# Initialize session state
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = 0

# Define challenges
challenges = [
    {
        "title": "Helsinki Cathedral (Helsingin tuomiokirkko)",
        "tasks": [
            "Take a photo of the most hardcore apostle & explain why",
            "Find and record the year the Cathedral was completed"
        ],
        "location": "Helsinki Cathedral"
    },
    {
        "title": "Market Square (Kauppatori)",
        "tasks": [
            "Find, picture and eat the 3 most Finnish snacks you can find (e.g., salmon soup, reindeer meat, or Karjalanpiirakka)",
            "Locate a food stall and discover the price of 'muikku' (small fried fish)"
        ],
        "location": "Market Square"
    },
    {
        "title": "Havis Amanda Fountain",
        "tasks": [
            "Find out the statue's nickname among locals (Manta)",
            "Ask a local about the tradition involving this fountain on May Day",
            "Take a video singing 'kiss from a rose' by Seal, with a Seal"
        ],
        "location": "Havis Amanda Fountain"
    },
    {
        "title": "Esplanadi Park (Esplanadin puisto)",
        "tasks": [
            "Find and photograph the statue of Finnish national poet Johan Ludvig Runeberg",
            "Bonus points: Identify the pastry named after him (Runeberg Torte)"
        ],
        "location": "Esplanadi Park"
    },
    {
        "title": "Kappeli Restaurant",
        "tasks": [
            "Ask the bartender for a recommended Finnish drink to share. Take a photo with your drinks",
            "Bonus: Selfie with the bartender"
        ],
        "location": "Kappeli Restaurant"
    },
    {
        "title": "Ateneum Art Museum",
        "tasks": [
            "Identify a famous Finnish artist whose works are exhibited here & record a Finnish person teaching you how to pronounce their name",
            "Bonus: Get creative: pose in the most interesting way outside the museum"
        ],
        "location": "Ateneum Art Museum"
    },
    {
        "title": "Senate Square (Senaatintori)",
        "tasks": [
            "Return promptly to Senate Square. Extra points if your team arrives first!"
        ],
        "location": "Senate Square"
    }
]

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# App title and description
st.title("Helsinki City Tour Challenge")
st.write("Complete each challenge to explore Helsinki's most famous landmarks!")

# Display current challenge
current = challenges[st.session_state.current_challenge]
st.header(f"Challenge {st.session_state.current_challenge + 1}: {current['title']}")
st.subheader(f"Location: {current['location']}")

# Display tasks
st.write("Tasks:")
for i, task in enumerate(current["tasks"], 1):
    st.write(f"{i}. {task}")

# File uploader for images/videos
uploaded_files = st.file_uploader(
    "Upload your photos/videos for this challenge",
    type=["jpg", "jpeg", "png", "mp4"],
    accept_multiple_files=True
)

# Text input for answers
answers = st.text_area("Enter your answers/observations for this challenge")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous Challenge") and st.session_state.current_challenge > 0:
        st.session_state.current_challenge -= 1
        st.rerun()

with col2:
    if st.button("Next Challenge") and st.session_state.current_challenge < len(challenges) - 1:
        st.session_state.current_challenge += 1
        st.rerun()

# Progress indicator
st.progress((st.session_state.current_challenge + 1) / len(challenges))
st.write(f"Challenge {st.session_state.current_challenge + 1} of {len(challenges)}")

# Save uploaded files and answers
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved {uploaded_file.name}")

if answers:
    st.success("Answers saved!") 