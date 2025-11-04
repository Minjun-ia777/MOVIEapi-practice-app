# app.py
import streamlit as st
import requests

# This API is free, fast, and needs no key.
BASE_URL = "https://dog.ceo/api/breeds/image/random"

st.set_page_config(layout="wide")
st.title("🐶 Random Dog Pic Generator")
st.write("Click the button for a new dog picture! (Using a reliable, no-key API)")

# This button is the only thing we need!
if st.button("Get a new dog!", type="primary"):
    
    try:
        # 1. Call the API
        response = requests.get(BASE_URL)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        
        # 2. Check the response and display the image
        if data["status"] == "success":
            image_url = data["message"]  # The image URL is in the "message" field
            
            st.image(image_url, caption="Here's a good dog!")
            st.write(f"Image URL: {image_url}") # Show the URL as well
        
        else:
            st.error("The API returned an error, but at least it's online!")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the Dog API. Error: {e}")
