# app.py
import streamlit as st
import requests
import datetime

# --- API Configuration ---
# We will get this from Streamlit Secrets
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except KeyError:
    st.error("OpenWeather API Key not found. Please add it to your Streamlit Secrets.")
    st.stop()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.set_page_config(layout="centered")
st.title("🌤️ Simple Weather Dashboard")

# --- City Input ---
city = st.text_input("Enter a city name:", "Seoul")

if st.button("Get Weather", type="primary"):
    if not city:
        st.warning("Please enter a city name.")
        st.stop()

    # --- API Call ---
    # Build the request parameters
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for errors (like 401, 404)
        
        data = response.json()

        # --- Display Results ---
        main = data["main"]
        weather = data["weather"][0]
        
        st.subheader(f"Weather in {data['name']}, {data['sys']['country']}")

        # Get icon URL
        icon_code = weather['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(icon_url, caption=weather['description'].title(), width=100)
        
        with col2:
            temp = main['temp']
            feels_like = main['feels_like']
            st.metric("Temperature", f"{temp}°C")
            st.write(f"**Feels like:** {feels_like:.1f}°C")

        st.divider()
        
        # More details in columns
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Humidity", f"{main['humidity']}%")
        col_b.metric("Pressure", f"{main['pressure']} hPa")
        col_c.metric("Wind Speed", f"{data['wind']['speed']} m/s")
        
        # st.write(data) # Uncomment this if you want to see all the raw data

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            st.error("API Key is incorrect or not yet active. (It can take up to 2 hours)")
        elif err.response.status_code == 404:
            st.error(f"Could not find weather for '{city}'. Check the spelling.")
        else:
            st.error(f"An HTTP error occurred: {err}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
