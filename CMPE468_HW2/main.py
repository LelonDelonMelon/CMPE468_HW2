import wave
import numpy as np
import matplotlib.pyplot as plt

wave_obj = wave.open("s5.wav", "rb")

sample_freq = wave_obj.getframerate()

windows_size = 5 / sample_freq

print("Sampling frequency: ", sample_freq, "Window size:", windows_size)

n_channels = wave_obj.getnchannels()

print("Number of channels:", n_channels)

n_samples = wave_obj.getnframes()

print("Sample size:", n_samples)

audio_length = n_samples / sample_freq

print("Audio length: ", audio_length)

sample_width = wave_obj.getsampwidth()

print("Sample width:", sample_width)

# signal bytes from wave obj:
signal_wave = wave_obj.readframes(n_samples)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)

# If stereo, use only the first channel
if n_channels == 2:
    signal_array = signal_array[::2]

# define window size and hop size
# win_size = int(sample_freq * 0.2)

# hop_size = int(win_size * 0.015)

win_size = 512
hop_size = 128

print("Hop_size", hop_size)
# calculate short-time energy using sliding window
ste = []
for i in range(0, len(signal_array) - win_size, hop_size):
    win = signal_array[i : i + win_size]
    energy = sum(np.power(win, 2)) / len(win)
    ste.append(energy)

# Plot waveform and STE in the same window using subplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
fig.subplots_adjust(bottom=0.2, left=0.1, hspace=0.4)

times = np.linspace(0, audio_length, num=len(signal_array))

ax1.plot(times, signal_array, label="Signal")
ax1.set_title("Waveform")
ax1.set_ylabel("Signal Value")
ax1.set_xlabel("Time (s)", labelpad=2)
ax1.set_xlim(0, audio_length)

ax1.legend()
times_ste = np.linspace(0, audio_length, num=len(ste))
ax2.plot(times_ste, ste, label="STE")
ax2.set_title("Short-time Energy")
ax2.set_ylabel("Energy")
ax2.set_xlabel("Time (s)")
ax2.set_xlim(0, audio_length)
plt.legend()
plt.show()
