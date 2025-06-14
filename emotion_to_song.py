import pandas as pd
from collections import defaultdict

def get_songs_by_emotion(emotion):
    try:
        # Read CSV
        songs_df = pd.read_csv("songs.csv")

        # Clean column names
        songs_df.columns = songs_df.columns.str.strip().str.lower()

        # Required columns check
        required_columns = ['emotion', 'language', 'platform', 'song']
        if not all(col in songs_df.columns for col in required_columns):
            print("Missing columns in songs.csv. Required: Emotion, Language, Platform, Song")
            return {}

        # Filter songs for the given emotion (case-insensitive)
        filtered = songs_df[songs_df['emotion'].str.strip().str.lower() == emotion.strip().lower()]

        # Organize by language → platform → list of songs
        result = defaultdict(lambda: defaultdict(list))
        for _, row in filtered.iterrows():
            lang = row['language'].strip().lower()
            platform = row['platform'].strip().lower()
            song = row['song'].strip()
            result[lang][platform].append(song)

        return result

    except Exception as e:
        print("Error loading songs:", e)
        return {}
