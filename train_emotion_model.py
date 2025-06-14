# train_emotion_model.py
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from utils import preprocess_pixels, build_emotion_model

# Load dataset
df = pd.read_csv('fer2013_training_oneshot.csv')

# Preprocess image data
pixels = df['pixels'].tolist()
x_data = np.array([preprocess_pixels(pix) for pix in pixels])
y_data = df.drop(columns=['pixels']).values

# Split into training and validation
x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

# Build and compile model
model = build_emotion_model(input_shape=(48, 48, 1), num_classes=y_data.shape[1])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(x_train, y_train, epochs=15, batch_size=64, validation_data=(x_val, y_val))

# Save model
model.save('emotion_model.h5')
print("Model trained and saved as 'emotion_model.h5'")
