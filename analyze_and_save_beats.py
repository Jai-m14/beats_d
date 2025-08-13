import librosa

def analyze_and_save(song_file, beats_py_path='beats.py'):
    y, sr = librosa.load(song_file)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print("Estimated tempo:", tempo)
    print("Detected {} beats.".format(len(beat_times)))
    # Write out the Python file
    with open(beats_py_path, "w") as f:
        f.write("beat_times = [\n")
        for t in beat_times:
            f.write(f"    {t:.8f},\n")
        f.write("]\n")
    print(f"Wrote beat times to {beats_py_path}")

if __name__ == "__main__":
    import sys
    # Example usage: python analyze_and_save_beats.py "songs/song2.mp3"
    song = sys.argv[1]
    analyze_and_save(song)
