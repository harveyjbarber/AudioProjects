import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
import ToneFunctions as tf
import Utils as ut

plt.close('all')

class Arpeggiator:
    
    def __init__(self, pitch_intervals, int_intervals, notes, time_sig=4, bpm=90,
                 fs=44100):
        
        self.pitch_intervals = pitch_intervals
        self.int_intervals = int_intervals
        self.notes = notes
        self.time_sig = time_sig
        self.bpm = bpm
        self.note_freqs = np.zeros_like(notes)
        self.fs = fs
        
        i = 0
        for note in notes:
            self.note_freqs[i] = tf.get_frequency_from_note(note)
            i += 1
            
        self.samples_per_beat = self.fs / (self.bpm / 60)
        self.samples_per_bar = self.samples_per_beat * self.time_sig
        
        
    def calculate_sample_intervals(self):
        
        intervals_cum = np.cumsum(self.int_intervals)
        intervals_tot = np.sum(intervals)
        
        return intervals_cum * (self.samples_per_bar / intervals_tot)
    
    def generate_waveform(self, seconds=5, n_harmonics=10):
        
        sample_intervals = self.calculate_sample_intervals().astype(int)
        
        t = np.linspace(0, seconds, self.fs * seconds)
        waveform = np.zeros_like(t)
        
        total_samples = seconds * self.fs
        
        total_bars = total_samples / self.samples_per_bar
        
        sample_intervals = np.insert(sample_intervals, 0, 0)
        remaining_samples = total_samples
        write_position = 0
        
        note_index = 0
        
        while(remaining_samples > sample_intervals[-1]):
            
            for i in range(sample_intervals.shape[0] - 1):
                    
                length = sample_intervals[i+1] - sample_intervals[i]
                pos1 = int(write_position + sample_intervals[i])
                pos2 = int(write_position + sample_intervals[i+1])
                waveform[pos1:pos2] = np.kaiser(length, 5) * tf.generate_n_sample_chord(self.notes[note_index], n_harmonics, length, self.fs)
                note_index += 1
                if note_index == len(self.note_freqs):
                    note_index = 0
                
            remaining_samples -= self.samples_per_bar
            write_position += self.samples_per_bar
                
        return waveform

        
save_destination = '../test/sines/arpg.wav'

intervals = [1, 2, 2, 2]

fs = 44100.

note = 28
notes = [40, 38, 39, 44]

seconds = 8

arpg = Arpeggiator(0, intervals, notes, time_sig=4, bpm=150)

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
