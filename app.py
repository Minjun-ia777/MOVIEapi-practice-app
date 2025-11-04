import streamlit as st
import requests

# --- API Key Configuration ---
# We will load this from Streamlit's Secrets
try:
    API_KEY = st.secrets["HIYEg4cAjPfAOOUs3saHuY2evmhoj60B"]
except KeyError:
    st.error("GIPHY_API_KEY not found. Please add it to your Streamlit Secrets.")
    st.stop()

# GIPHY API Search Endpoint
BASE_URL = "https://api.giphy.com/v1/gifs/search"

st.set_page_config(layout="wide")
st.title("Search the GIPHY-verse! 🌌")
st.write("A simple app to practice using an API key with Streamlit.")

st.divider()

# --- Search UI ---
search_query = st.text_input("What are you looking for?", "Cats")

col1, col2 = st.columns([3, 1])

with col1:
    limit = st.slider("How many GIFs do you want?", 5, 50, 10)

with col2:
    # This empty space helps align the button
    st.write("")
    st.write("")
    search_button = st.button("Search", type="primary", use_container_width=True)


# --- API Call and Display ---
if search_button:
    if not search_query:
        st.warning("Please enter a search term.")
        st.stop()

    # Build the parameters for the API request
    params = {
        "api_key": API_KEY,
        "q": search_query,
        "limit": limit,
        "offset": 0,  # Start from the beginning
        "rating": "g", # Keep it family-friendly
        "lang": "en"
    }
    
    try:
        # 1. Call the API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for errors
        
        data = response.json()
        
        # 2. Check if we got any results
        if not data.get("data"):
            st.warning(f"No GIFs found for '{search_query}'. Try another search!")
            st.stop()

        # 3. Display the GIFs in a cool grid
        st.success(f"Here are your {len(data['data'])} GIFs!")
        
        # Create 5 columns for the grid
        cols = st.columns(5)
        
        for i, gif in enumerate(data["data"]):
            gif_url = gif["images"]["fixed_height"]["url"]
            
            # Place the image in the next available column
            with cols[i % 5]: # (0, 1, 2, 3, 4, 0, 1, ...)
                st.image(gif_url, caption=f"GIF {i+1}", use_column_width=True)

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            st.error("Invalid API Key. Make sure your Streamlit Secret is correct.")
        else:
            st.error(f"An HTTP error occurred: {err}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
