import streamlit as st
import json
from PIL import Image
import os

# Define valid team passwords
TEAM_PASSWORDS = {
    "team1pass": "Team 1",
    "team2pass": "Team 2"
}

ADMIN_PASSWORD = "adminpass"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'team_name' not in st.session_state:
    st.session_state.team_name = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Initialize or load team progress
TEAM_PROGRESS_FILE = "data/team_progress.json"
if not os.path.exists(TEAM_PROGRESS_FILE):
    initial_progress = {
        "teams": {
            "Team 1": {"current_challenge": 0, "answers": {}},
            "Team 2": {"current_challenge": 0, "answers": {}}
        }
    }
    with open(TEAM_PROGRESS_FILE, "w") as f:
        json.dump(initial_progress, f)

def load_team_progress():
    with open(TEAM_PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_team_progress(progress):
    with open(TEAM_PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

# Define challenges with UI configurations
challenges = [
    {
        "title": "Helsinki Cathedral (Helsingin tuomiokirkko)",
        "tasks": [
            "Take a photo of the most hardcore apostle & explain why",
            "Find and record the year the Cathedral was completed"
        ],
        "location": "Helsinki Cathedral",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your photos of the apostles"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "Explain your choice of apostle"
            },
            "number_input": {
                "enabled": True,
                "label": "Enter the year the Cathedral was completed",
                "min_value": 1800,
                "max_value": 1900
            }
        }
    },
    {
        "title": "Market Square (Kauppatori)",
        "tasks": [
            "Find, picture and eat the 3 most Finnish snacks you can find (e.g., salmon soup, reindeer meat, or Karjalanpiirakka)",
            "Locate a food stall and discover the price of 'muikku' (small fried fish)"
        ],
        "location": "Market Square",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload photos of the snacks you tried"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "Describe the snacks you tried"
            },
            "number_input": {
                "enabled": True,
                "label": "Enter the price of muikku (in euros)",
                "min_value": 0.0,
                "max_value": 50.0,
                "step": 0.5
            }
        }
    },
    {
        "title": "Havis Amanda Fountain",
        "tasks": [
            "Find out the statue's nickname among locals (Manta)",
            "Ask a local about the tradition involving this fountain on May Day",
            "Take a video singing 'kiss from a rose' by Seal, with a Seal"
        ],
        "location": "Havis Amanda Fountain",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png", "mp4"],
                "multiple": True,
                "label": "Upload your photos and videos"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "Share what you learned about the May Day tradition"
            },
            "radio": {
                "enabled": True,
                "label": "What is the statue's nickname?",
                "options": ["Manta", "Amanda", "Havis", "Seal"]
            }
        }
    },
    {
        "title": "Esplanadi Park (Esplanadin puisto)",
        "tasks": [
            "Find and photograph the statue of Finnish national poet Johan Ludvig Runeberg",
            "Bonus points: Identify the pastry named after him (Runeberg Torte)"
        ],
        "location": "Esplanadi Park",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": False,
                "label": "Upload a photo with the statue"
            },
            "checkbox": {
                "enabled": True,
                "label": "Did you find the Runeberg Torte?",
                "options": ["Yes, I found it!", "No, I couldn't find it"]
            }
        }
    },
    {
        "title": "Kappeli Restaurant",
        "tasks": [
            "Ask the bartender for a recommended Finnish drink to share. Take a photo with your drinks",
            "Bonus: Selfie with the bartender"
        ],
        "location": "Kappeli Restaurant",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your drink photos"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "What drink did you try? How was it?"
            }
        }
    },
    {
        "title": "Ateneum Art Museum",
        "tasks": [
            "Identify a famous Finnish artist whose works are exhibited here & record a Finnish person teaching you how to pronounce their name",
            "Bonus: Get creative: pose in the most interesting way outside the museum"
        ],
        "location": "Ateneum Art Museum",
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png", "mp4"],
                "multiple": True,
                "label": "Upload your photos and videos"
            },
            "selectbox": {
                "enabled": True,
                "label": "Which Finnish artist did you learn about?",
                "options": ["Akseli Gallen-Kallela", "Hugo Simberg", "Helene Schjerfbeck", "Albert Edelfelt", "Other"]
            }
        }
    },
    {
        "title": "Senate Square (Senaatintori)",
        "tasks": [
            "Return promptly to Senate Square. Extra points if your team arrives first!"
        ],
        "location": "Senate Square",
        "ui_elements": {
            "slider": {
                "enabled": True,
                "label": "How many minutes did it take you to return?",
                "min_value": 0,
                "max_value": 60,
                "step": 1
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "Any final thoughts about the tour?"
            }
        }
    }
]

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Login screen
if not st.session_state.authenticated:
    st.title("Helsinki City Tour Challenge")
    st.write("Please enter your team password to begin:")
    
    password = st.text_input("Team Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            st.rerun()
        elif password in TEAM_PASSWORDS:
            st.session_state.authenticated = True
            st.session_state.team_name = TEAM_PASSWORDS[password]
            st.rerun()
        else:
            st.error("Invalid password. Please try again.")
    st.stop()

# Load team progress
team_progress = load_team_progress()

# Admin view
if st.session_state.is_admin:
    st.title("Admin Dashboard")
    
    # Display team progress
    for team_name, team_data in team_progress["teams"].items():
        st.header(f"Team: {team_name}")
        st.write(f"Current Challenge: {team_data['current_challenge'] + 1} of {len(challenges)}")
        st.progress((team_data['current_challenge'] + 1) / len(challenges))
        
        # Display answers
        if team_data['answers']:
            st.subheader("Answers:")
            for answer_key, answer_value in team_data['answers'].items():
                st.write(f"**{answer_key}**:")
                # Check if the answer is a list of files (image uploads)
                if isinstance(answer_value, list):
                    for filename in answer_value:
                        file_path = os.path.join("uploads", f"{team_name}_{filename}")
                        if os.path.exists(file_path):
                            try:
                                image = Image.open(file_path)
                                st.image(image, caption=filename, use_column_width=True)
                            except Exception as e:
                                st.write(f"Could not display {filename}: {str(e)}")
                        else:
                            st.write(f"File not found: {filename}")
                else:
                    st.write(answer_value)
        else:
            st.write("No answers submitted yet.")
        
        st.markdown("---")
    
    # Clear data button
    if st.button("Clear All Team Data"):
        initial_progress = {
            "teams": {
                "Team 1": {"current_challenge": 0, "answers": {}},
                "Team 2": {"current_challenge": 0, "answers": {}}
            }
        }
        save_team_progress(initial_progress)
        st.success("All team data has been cleared!")
        st.rerun()
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.rerun()
    
    st.stop()

# Initialize session state with team's progress
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = team_progress["teams"][st.session_state.team_name]["current_challenge"]
if 'answers' not in st.session_state:
    st.session_state.answers = team_progress["teams"][st.session_state.team_name]["answers"]

def validate_challenge_completion(challenge, answers):
    """Check if all required fields for the current challenge are completed."""
    missing_fields = []
    challenge_key = challenge['title']
    
    for element_type, config in challenge['ui_elements'].items():
        if config.get('enabled', False):
            field_key = f"{challenge_key}_{element_type}"
            if field_key not in answers or not answers[field_key]:
                missing_fields.append(config.get('label', element_type))
    
    return missing_fields

# App title and description
st.title("Helsinki City Tour Challenge")
st.write(f"Welcome, {st.session_state.team_name}!")

# Show other teams' progress
st.sidebar.title("Team Progress")
for team_name, team_data in team_progress["teams"].items():
    st.sidebar.write(f"{team_name}: Challenge {team_data['current_challenge'] + 1} of {len(challenges)}")
    st.sidebar.progress((team_data['current_challenge'] + 1) / len(challenges))

# Add update button
if st.sidebar.button("Refresh Progress"):
    team_progress = load_team_progress()
    st.rerun()

# Display current challenge
current = challenges[st.session_state.current_challenge]
st.header(f"Challenge {st.session_state.current_challenge + 1}: {current['title']}")
st.subheader(f"Location: {current['location']}")

# Display tasks
st.write("Tasks:")
for i, task in enumerate(current["tasks"], 1):
    st.write(f"{i}. {task}")

# Dynamic UI rendering based on challenge configuration
if 'ui_elements' in current:
    for element_type, config in current['ui_elements'].items():
        if config.get('enabled', False):
            if element_type == 'file_upload':
                uploaded_files = st.file_uploader(
                    config.get('label', "Upload your files"),
                    type=config.get('types', ["jpg", "jpeg", "png"]),
                    accept_multiple_files=config.get('multiple', False)
                )
                if uploaded_files:
                    # Convert to list if single file
                    if not isinstance(uploaded_files, list):
                        uploaded_files = [uploaded_files]
                    
                    # Save files and track in session state
                    saved_files = []
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join("uploads", f"{st.session_state.team_name}_{uploaded_file.name}")
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        saved_files.append(uploaded_file.name)
                        st.success(f"Saved {uploaded_file.name}")
                    
                    # Update session state with uploaded files
                    st.session_state.answers[f"{current['title']}_{element_type}"] = saved_files
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
            
            elif element_type == 'text_input':
                if config.get('type') == 'text_area':
                    answer = st.text_area(config.get('label', "Enter your answer"))
                else:
                    answer = st.text_input(config.get('label', "Enter your answer"))
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'number_input':
                answer = st.number_input(
                    config.get('label', "Enter a number"),
                    min_value=config.get('min_value', 0),
                    max_value=config.get('max_value', 100),
                    step=config.get('step', 1)
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'radio':
                answer = st.radio(
                    config.get('label', "Select an option"),
                    options=config.get('options', [])
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'checkbox':
                answer = st.checkbox(config.get('label', "Check if completed"))
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'selectbox':
                answer = st.selectbox(
                    config.get('label', "Select an option"),
                    options=config.get('options', [])
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'slider':
                answer = st.slider(
                    config.get('label', "Select a value"),
                    min_value=config.get('min_value', 0),
                    max_value=config.get('max_value', 100),
                    step=config.get('step', 1)
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous Challenge") and st.session_state.current_challenge > 0:
        st.session_state.current_challenge -= 1
        team_progress["teams"][st.session_state.team_name]["current_challenge"] = st.session_state.current_challenge
        save_team_progress(team_progress)
        st.rerun()

with col2:
    # Check if all required fields are completed
    missing_fields = validate_challenge_completion(current, st.session_state.answers)
    
    if missing_fields:
        st.warning("Please complete all required fields before proceeding:")
        for field in missing_fields:
            st.write(f"• {field}")
    
    if st.button("Next Challenge", disabled=bool(missing_fields)) and st.session_state.current_challenge < len(challenges) - 1:
        st.session_state.current_challenge += 1
        team_progress["teams"][st.session_state.team_name]["current_challenge"] = st.session_state.current_challenge
        save_team_progress(team_progress)
        st.rerun()

# Progress indicator
st.progress((st.session_state.current_challenge + 1) / len(challenges))
st.write(f"Challenge {st.session_state.current_challenge + 1} of {len(challenges)}")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.team_name = None
    st.rerun() 