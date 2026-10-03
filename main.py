import pyaudio,wave,speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

# Open microphone
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024
)

print("🎤 Recording... Press Ctrl+C to stop.")

frames = []

try:
    while True:
        data = stream.read(1024)
        frames.append(data)

except KeyboardInterrupt:
    print("✅ Recording stopped.")

stream.stop_stream()
stream.close()
p.terminate()

# Convert audio into numbers
audio = b"".join(frames)
with wave.open("recording.wav","wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    f.writeframes(audio)
data=sr.AudioData(audio,16000,2)
print(sr.Recognizer().recognize_google(data))
samples = np.frombuffer(audio, dtype=np.int16)

# Create time axis
time = np.linspace(0, len(samples) / 16000, len(samples))

# Show waveform
plt.plot(time, samples)
plt.title("Your Voice Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.show()