import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile

plt.close('all')


def get_frequency_from_note(note_n):
    """
    Give a note on the piano, returns the frequency in Hz of that note.
    """
    
    return ((2)**(1/12))**(note_n-49) * 440


def generate_n_sample_sine(frequency, n_samples, sample_rate=44100):
    
    samples = np.arange(0, n_samples, 1)
    
    t = samples * (1/sample_rate)
    
    return np.sin(2 * np.pi * frequency * t)


def generate_n_sample_sine_with_harmonics(frequency, n_harmonics, n_samples, sample_rate=44100):
    
    # Time vector
    samples = np.arange(0, n_samples, 1)
    
    t = samples * (1/sample_rate)
    
    decay = 0.1
    decay_factor = 5
    
    # First harmonic
    output = np.sin(2 * np.pi * frequency * t)
    
    for i in range(2, n_harmonics+2):

        output += decay * np.sin(2 * np.pi * i * frequency * t)
        decay = decay / decay_factor
        
    return output


def mag2dB(mag):
    
    return 20*np.log10(np.abs(mag))


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
            self.note_freqs[i] = get_frequency_from_note(note)
            i += 1
            
        self.samples_per_beat = self.fs / (self.bpm / 60)
        self.samples_per_bar = self.samples_per_beat * self.time_sig
        
  
        
    def CalculateSampleIntervals(self):
        
        intervals_cum = np.cumsum(self.int_intervals)
        intervals_tot = np.sum(intervals)
        
        return intervals_cum * (self.samples_per_bar / intervals_tot)
    
    def GenerateWaveform(self, seconds=5, n_harmonics=10):
        
        sample_intervals = self.CalculateSampleIntervals().astype(int)
        
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
                waveform[int(write_position + sample_intervals[i]):int(write_position + sample_intervals[i+1])] = np.kaiser(length, 5) * generate_n_sample_sine_with_harmonics(self.note_freqs[note_index], n_harmonics, length, self.fs)
                note_index += 1
                if note_index == len(self.note_freqs):
                    note_index = 0
                
            remaining_samples -= self.samples_per_bar
            write_position += self.samples_per_bar
                
        return waveform

        
save_destination = '../test/sines/arpg.wav'

intervals = [2, 2, 3, 2, 4, 3, 3, 2]

fs = 44100.

note = 28
notes = [40, 38, 42, 37, 44, 42, 47, 49, 44]

seconds = 8

arpg = Arpeggiator(0, intervals, notes, time_sig=4, bpm=150)

data = arpg.GenerateWaveform(seconds, 1)
    

chord = [40, 44, 47, 49]

for i in chord:
    freq = get_frequency_from_note(i)
    data += 0.1 * generate_n_sample_sine_with_harmonics(freq, 10, seconds * fs, fs)

data_f = np.fft.rfft(data)
freqs = np.fft.rfftfreq(data.shape[0]) * fs

wavfile.write(save_destination, int(fs), data)

plt.figure()
plt.subplot(211)
plt.plot(data)
plt.subplot(212)
plt.semilogx(freqs, mag2dB(data_f))
plt.xlim([20, fs/2])
