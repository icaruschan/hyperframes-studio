import wave
import struct
import math

def analyze_audio(file_path):
    wf = wave.open(file_path, 'rb')
    sample_rate = wf.getframerate()
    num_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    n_frames = wf.getnframes()
    
    print(f"Sample Rate: {sample_rate} Hz, Channels: {num_channels}, Width: {sampwidth} bytes, Frames: {n_frames}")
    
    # 50ms window size in samples
    window_ms = 50
    samples_per_window = int(sample_rate * (window_ms / 1000.0))
    
    # Read raw audio frames
    raw_data = wf.readframes(n_frames)
    wf.close()
    
    # Parse frames
    fmt = f"{n_frames * num_channels}h"
    try:
        samples = struct.unpack(fmt, raw_data)
    except Exception as e:
        print("Error unpacking raw data:", e)
        return
        
    print("\n--- Audio Energy Profile (First 3 Seconds) ---")
    print(f"{'Time (s)':<10} | {'RMS Value':<10} | {'Visual Peak'}")
    print("-" * 50)
    
    max_val = 32768.0
    for idx, i in enumerate(range(0, len(samples), samples_per_window)):
        window_samples = samples[i:i+samples_per_window]
        if not window_samples:
            break
        
        # Calculate RMS (Root Mean Square) energy
        sum_squares = sum((s / max_val) ** 2 for s in window_samples)
        rms = math.sqrt(sum_squares / len(window_samples))
        
        time_sec = (idx * window_ms) / 1000.0
        if time_sec > 12.0:
            break
            
        bar = "#" * int(rms * 100)
        print(f"{time_sec:<10.2f} | {rms:<10.4f} | {bar}")

if __name__ == "__main__":
    analyze_audio("assets/audio_temp.wav")
