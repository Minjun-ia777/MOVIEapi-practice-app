# app.py
import streamlit as st
import requests

# This is the API endpoint. No key needed!
BASE_URL = "https://www.boredapi.com/api/activity/"

st.set_page_config(layout="wide")
st.title("🥱 The Cure for Boredom")
st.write("Can't decide what to do? Let a public API decide for you.")

st.divider()

# --- Interactive Controls ---
st.header("What kind of activity are you looking for?")

# Create columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    # Dropdown to select a type of activity
    activity_type = st.selectbox("Select a type (optional):", 
                                 ["(any)", "education", "recreational", "social", 
                                  "diy", "charity", "cooking", "relaxation", 
                                  "music", "busywork"])

with col2:
    # Slider to select number of people
    participants = st.slider("How many people are involved?", 1, 5, 1)


# --- API Call Button ---
if st.button("Find me an activity!", type="primary"):
    
    # 1. Build the API query string
    params = {}
    if activity_type != "(any)":
        params["type"] = activity_type
    
    params["participants"] = participants
    
    try:
        # 2. Call the API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        
        # 3. Display the result
        if data.get("activity"):
            st.success("Here's your idea!")
            
            st.subheader(data["activity"])
            
            st.write(f"**Type:** {data['type'].title()}")
            
            if data.get("link"):
                st.write(f"**Learn more:** {data['link']}")
        
        elif data.get("error"):
            st.warning(f"No activity found with those settings. Try being less specific!")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the Bored API. Error: {e}")
