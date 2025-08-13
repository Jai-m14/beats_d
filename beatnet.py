from BeatNet.BeatNet import BeatNet

# Choose offline mode for best accuracy
estimator = BeatNet(1, mode='offline', inference_model='DBN', plot=[], thread=False)

# Path to your .wav music file
audio_file = "your_song.wav"

# Process the file and obtain beat times
beat_times = estimator.process(audio_file)

# Print or use your beat times:
for t in beat_times:
    print(f"Beat at: {t:.3f} sec")
