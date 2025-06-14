import streamlit as st
from PIL import Image
from predict_emotion import predict_emotion
from emotion_to_song import get_songs_by_emotion

st.set_page_config(page_title="Emotion-Based Song Recommender", layout="centered")
st.title("🎵 Emotion-Based Song Recommender")

st.write("Upload a photo or use webcam to detect your emotion and get personalized multilingual song suggestions.")

# Image input section
image = None
option = st.radio("Choose input method:", ["Upload Image", "Use Webcam"])

if option == "Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_column_width=True)

elif option == "Use Webcam":
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer:
        image = Image.open(img_file_buffer)
        st.image(image, caption="Webcam Snapshot", use_column_width=True)

# Process the image and recommend songs
if image and st.button("🎯 Detect Emotion & Recommend Songs"):
    emotion = predict_emotion(image)

    if emotion:
        st.subheader(f"Detected Emotion: **{emotion.upper()}**")

        songs = get_songs_by_emotion(emotion)
        if songs:
            for lang, platforms in songs.items():
                st.markdown(f"### 🌐 {lang.capitalize()} Songs")
                for platform, song_list in platforms.items():
                    st.markdown(f"**{platform.capitalize()}**:")
                    for song in song_list:
                        st.markdown(f"- {song}")
        else:
            st.warning("No songs found for the detected emotion.")
    else:
        st.error("Emotion could not be detected. Please try another image.")
