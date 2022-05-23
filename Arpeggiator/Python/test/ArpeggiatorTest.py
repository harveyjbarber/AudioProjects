import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
import Arpeggiator as ap
import Utils as ut
import NotesEnum as NoteEnum

Note = NoteEnum.Note

plt.close('all')


save_destination = './sines/arpg.wav'

intervals = [1, 2, 2, 2, 1]

fs = 44100.

notes = [Note.A4, Note.C5, Note.Fs4, Note.D5, Note.E5]

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