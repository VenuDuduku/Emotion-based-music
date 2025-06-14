import pandas as pd

def get_songs_by_emotion(emotion):
    try:
        df = pd.read_csv("songs.csv")
        required_cols = {"Emotion", "Language", "Platform", "Song", "Link"}
        if not required_cols.issubset(df.columns):
            raise ValueError("Missing required columns in songs.csv")

        filtered_df = df[df['Emotion'].str.lower() == emotion.lower()]
        return filtered_df.to_dict(orient="records")  # ✅ list of dicts
    except Exception as e:
        print("Error loading songs:", e)
        return []
