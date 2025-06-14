import streamlit as st
from PIL import Image
from predict_emotion import predict_emotion
from emotion_to_song import get_songs_by_emotion

st.set_page_config(page_title="Emotion-Based Song Recommender", layout="centered")

st.title("🎵 Emotion-Based Song Recommender")
st.markdown("Upload or capture your face image to detect emotion and get personalized song suggestions.")

# --- Input Method Selection ---
input_method = st.radio("Select Input Method:", ["📤 Upload Image", "📸 Use Webcam"])

image = None

if input_method == "📤 Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

elif input_method == "📸 Use Webcam":
    captured_image = st.camera_input("Capture a photo")
    if captured_image:
        image = Image.open(captured_image)
        st.image(image, caption="Captured Image", use_column_width=True)

# --- Language Filter ---
language_choice = st.selectbox("🌐 Preferred Language:", 
                               options=["All", "Telugu", "Hindi", "English", "Malayalam"])

# --- Process if Image Exists ---
if image:
    emotion = predict_emotion(image)

    if emotion:
        st.success(f"🎭 You look **{emotion.capitalize()}** today! Here's your mood-based playlist:")

        # Get songs
        songs = get_songs_by_emotion(emotion)

        # Filter by language
        if language_choice != "All":
            songs = [s for s in songs if s['Language'].lower() == language_choice.lower()]

        if songs:
            st.markdown("### 🎶 Recommended Songs:")
            for song in songs:
                song_name = song.get("Song", "Unknown")
                platform = song.get("Platform", "Unknown").capitalize()
                language = song.get("Language", "Unknown").capitalize()
                link = song.get("Link", "#")

                icon = "🔴" if "youtube" in link.lower() else "🎵" if "spotify" in link.lower() else "🎧"

                st.markdown(f'<a href="{link}" target="_blank" style="text-decoration: none; font-size: 18px;">{icon} <b>{song_name}</b> ({language}, {platform})</a>', unsafe_allow_html=True)
        else:
            st.warning(f"No songs found for **{emotion}** in **{language_choice}**.")
    else:
        st.error("⚠️ Could not detect emotion. Try using a clearer image.")
