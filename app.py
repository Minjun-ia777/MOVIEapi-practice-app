# app.py
import streamlit as st
import requests

# --- API Configuration ---
# DO NOT hardcode your API key here. We will use Streamlit Secrets.
try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except KeyError:
    st.error("TMDb API Key not found. Please add it to your Streamlit Secrets.")
    st.stop()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# --- Helper Functions to Call TMDb API ---

def search_movies(query):
    """Search for movies based on a query."""
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": query, "language": "en-US"}
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_movie_details(movie_id):
    """Get detailed information for a specific movie."""
    details_url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(details_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_movie_trailer(movie_id):
    """Get the YouTube trailer key for a movie."""
    videos_url = f"{BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(videos_url, params=params)
    if response.status_code == 200:
        videos = response.json().get("results", [])
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return video["key"]
    return None

# --- Streamlit App Layout ---

st.set_page_config(layout="wide")
st.title("🎬 Super Movie Database")
st.write("Find details, ratings, and trailers for any movie!")

# --- Search Bar ---
search_query = st.text_input("Search for a movie...", "")

if not search_query:
    st.info("Start by searching for a movie title.")
    st.stop()

# --- Search Results ---
movie_list = search_movies(search_query)

if not movie_list:
    st.warning("No movies found for that query.")
    st.stop()

# --- Movie Selection ---
# Use movie titles for the selectbox, but store the ID
movie_titles = [f"{movie['title']} ({movie['release_date'][:4]})" for movie in movie_list if 'release_date' in movie and movie['release_date']]
movie_ids = {f"{movie['title']} ({movie['release_date'][:4]})": movie['id'] for movie in movie_list if 'release_date' in movie and movie['release_date']}

selected_movie_title = st.selectbox("Select a movie from the results:", movie_titles)

if selected_movie_title:
    selected_movie_id = movie_ids[selected_movie_title]
    
    # Fetch "super complete" details
    details = get_movie_details(selected_movie_id)
    
    if details:
        # --- Display Movie Details ---
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display Poster
            if details["poster_path"]:
                poster_url = f"{IMAGE_BASE_URL}{details['poster_path']}"
                st.image(poster_url, caption=details["title"])
            else:
                st.write("No poster available.")

        with col2:
            # Display Title and Tagline
            st.title(details["title"])
            if details["tagline"]:
                st.subheader(f"_{details['tagline']}_")

            # Display Rating, Duration, and Release Date
            rating = f"⭐ {details['vote_average']:.1f}/10"
            duration = f"⏳ {details['runtime']} minutes"
            release = f"🗓️ {details['release_date']}"
            st.write(f"{rating}  |  {duration}  |  {release}")

            # Display Genres
            genres = [genre["name"] for genre in details["genres"]]
            st.write(f"**Genres:** {', '.join(genres)}")
            
            # Display Overview
            st.header("Overview")
            st.write(details["overview"])

        # --- Display Trailer ---
        trailer_key = get_movie_trailer(selected_movie_id)
        if trailer_key:
            st.divider()
            st.header("Watch the Trailer")
            trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
            st.video(trailer_url)
        else:
            st.write("No trailer found.")
