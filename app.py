# app.py
import streamlit as st
import googleapiclient.discovery
import isodate # To parse video duration

# --- API Configuration ---
try:
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
except KeyError:
    st.error("YouTube API Key not found. Please add it to your Streamlit Secrets.")
    st.stop()

# --- Helper Function to Parse Duration ---
def parse_duration(duration_str):
    """Converts YouTube's ISO 8601 duration string (e.g., 'PT2M30S') 
       into a human-readable format (e.g., '2:30')."""
    duration = isodate.parse_duration(duration_str)
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"

# --- Main App ---

st.set_page_config(layout="wide")
st.title("🔥 Today's Top 25 Trending YouTube Videos")
st.write("This app uses the YouTube Data API to show today's trending videos (US).")

try:
    # 1. Build the YouTube API service
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY)

    # 2. Make the API request for "most popular" (trending) videos
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="US", # You can change this to your country code (e.g., "KR")
        maxResults=25
    )
    
    # 3. Execute the request
    # This is the 1-unit API call. We cache it so it doesn't re-run every second.
    @st.cache_data(ttl=3600) # Cache for 1 hour
    def get_trending_videos():
        response = request.execute()
        return response.get("items", [])

    videos = get_trending_videos()

    if not videos:
        st.warning("No trending videos found. The API might be down.")
        st.stop()

    # 4. Display the videos in a grid
    cols = st.columns(3) # Create 3 columns
    
    for i, video in enumerate(videos):
        # Get all the details
        snippet = video["snippet"]
        stats = video["statistics"]
        content = video["contentDetails"]
        
        title = snippet["title"]
        channel = snippet["channelTitle"]
        thumbnail_url = snippet["thumbnails"]["medium"]["url"]
        
        # Safely get view count and format it
        view_count = int(stats.get("viewCount", 0))
        
        # Parse the duration
        duration = parse_duration(content["duration"])

        # Display in the next available column
        with cols[i % 3]: # Cycles through columns 0, 1, 2
            st.subheader(title)
            st.image(thumbnail_url)
            st.write(f"**By:** {channel}")
            st.write(f"**Duration:** {duration}")
            st.write(f"**Views:** {view_count:,.0f}") # Formats 1000000 -> 1,000,000
            st.link_button("Watch on YouTube", f"https://www.youtube.com/watch?v={video['id']}")
            st.divider()

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.info("This can happen if the API key is incorrect or the daily quota has been exceeded.")
