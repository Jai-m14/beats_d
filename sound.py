import librosa

# Load your music file (mp3, wav supported)
y, sr = librosa.load("song2.mp3")

# Run the beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Convert frame indices to timestamps (seconds)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

print("Estimated tempo:", tempo)
print("Beat times (seconds):", beat_times)
