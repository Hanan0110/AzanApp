from flask import Flask, render_template, jsonify
import time
import pygame
import pandas as pd

app = Flask(__name__)

# Load the data from CSV into a pandas DataFrame
df = pd.read_csv('PrayerTimes.csv')

# Initialize pygame mixer
pygame.mixer.init()

# Function to play audio from a local file
def play_audio_from_file(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Variable to track whether Azan is playing
azan_playing = False

# Route to get the live time with seconds
@app.route('/live-time')
def get_live_time():
    global azan_playing

    # Get today's date
    today_date = time.strftime("%d")
    # Filter the DataFrame for today's data
    today_data = df[df['MARCH'] == int(today_date)]

    current_time = time.strftime("%I:%M:%S %p")  # Format: 12-hour with seconds and AM/PM
    current_time_without_seconds = time.strftime("%I:%M")

    if current_time_without_seconds.startswith("0"):
        current_time_without_seconds = current_time_without_seconds[1:]

    if current_time_without_seconds == today_data['FAJR'].values[0] and not azan_playing:
        play_audio_from_file("static/Fajr.mp3")  # Play Azan MP3 if time matches
        azan_playing = True  
    elif (current_time_without_seconds == today_data['DHUHR'].values[0] or \
        current_time_without_seconds == today_data['ASR'].values[0] or \
        current_time_without_seconds == today_data['MAGHRIB'].values[0] or \
        current_time_without_seconds == today_data['ISHA'].values[0]) and not azan_playing:
        play_audio_from_file("static/Azan.mp3")  # Play Azan MP3 if time matches
        azan_playing = True  

    elif azan_playing and not pygame.mixer.music.get_busy():
        azan_playing = False

    return jsonify({'live_time': current_time,'FAJR':today_data['FAJR'].values[0],'DHUHR':today_data['DHUHR'].values[0],'ASR':today_data['ASR'].values[0],'MAGHRIB':today_data['MAGHRIB'].values[0],'ISHA':today_data['ISHA'].values[0]})

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
