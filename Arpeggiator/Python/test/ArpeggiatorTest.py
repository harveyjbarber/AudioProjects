import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
import Arpeggiator as ap
import Utils as ut


plt.close('all')


save_destination = '../test/sines/arpg.wav'

intervals = [1, 2, 2, 2]

fs = 44100.

note = 28
notes = [40, 38, 39, 44]

seconds = 8

arpg = ap.Arpeggiator(0, intervals, notes, time_sig=4, bpm=150)

data = arpg.generate_waveform(seconds, 1)


data_f = np.fft.rfft(data)
freqs = np.fft.rfftfreq(data.shape[0]) * fs

wavfile.write(save_destination, int(fs), data)

plt.figure()
plt.subplot(211)
plt.plot(data)
plt.subplot(212)
plt.semilogx(freqs, ut.mag2db(data_f))
plt.xlim([20, fs/2])