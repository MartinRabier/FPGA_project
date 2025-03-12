#fréquence d'échantillonage ECG à 360HZ; période 2.8ms
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin, lfilter, find_peaks,butter,filtfilt

file = open("waveform_example_ecg.csv","r")
file.readline()


#heartbeats extraction and plot
nb_beats = 10
ecg = []
merged =[]
ecg_freq = 360
for i in range(nb_beats):
    test = file.readline()
    ecg = [int(test[i:i+2], 16) for i in range(0, len(test)-1, 2)]
    merged +=ecg

timestamp = np.linspace(0,nb_beats*(181/ecg_freq),nb_beats*181)
num_taps = 31
cutoff_freq = 30
fir_coeff = firwin(num_taps, cutoff_freq, fs=ecg_freq, pass_zero='lowpass')
filtered_signal = lfilter(fir_coeff, 1.0, merged)
peaks, _ = find_peaks(filtered_signal, height=200)
print(peaks)
interval = (timestamp[peaks[-1]]-timestamp[peaks[0]])/(nb_beats-1)
BPM = 60/interval
print(f"moyenne des {nb_beats-1} intervalles = {interval} d'ou frequence cardiaque a {BPM}")




'''
# Tracé du signal ECG
plt.figure(figsize=(16, 14))
plt.subplot(2,1,1)
plt.plot(timestamp,merged, label="ECG Signal", color="blue")
plt.xlabel("Temps (échantillons)")
plt.ylabel("Amplitude")
plt.title("filtered ECG signal")
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(timestamp,filtered_signal, label="filtered ECG signal", color="red")
plt.xlabel("Temps (échantillons)")
plt.ylabel("Amplitude")
plt.title("filtered ECG signal")
plt.legend()
plt.grid(True)


plt.subplots_adjust(hspace=0.4)
plt.show()
'''


#identification des cardiopathies
#soit un signal
test = file.readline()
extracted = [int(test[i:i+2], 16) for i in range(0, len(test)-1, 2)]
    
P = extracted[0:22]
PR = extracted[22:55]
QRS = extracted[55:73]
ST = extracted[73:96]
T = extracted[96:137]
QT = extracted[137:180]