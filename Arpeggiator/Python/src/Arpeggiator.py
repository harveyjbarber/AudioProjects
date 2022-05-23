import numpy as np
import ToneFunctions as tf

class Arpeggiator:
    """
    A class to perform arpeggiation of different input notes or chords.
    """
    
    def __init__(self, pitch_intervals, int_intervals, notes, time_sig=4, bpm=90,
                 fs=44100):
        """
        Initialise the class.

        Parameters
        ----------
        pitch_intervals : TYPE
            TODO
        int_intervals : list
            A list containing integer values to divide the bar into.
        notes : list
            A list of notes to arpeggiate through.
        time_sig : int, optional
            The beats per bar. The default is 4.
        bpm : int, optional
            Beats per minute. The default is 90.
        fs : float, optional
            The sample rate. The default is 44100.
        """
        
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
        """
        Convert the integer bar subdivisions into sample indexes.

        Returns
        -------
        ndarry
            An array of the sample indexes at which to change note.

        """
        
        intervals_cum = np.cumsum(self.int_intervals)
        intervals_tot = np.sum(self.int_intervals)
        
        return intervals_cum * (self.samples_per_bar / intervals_tot)
    
    def generate_waveform(self, seconds=5, n_harmonics=10):
        """
        Generate a waveform using the parameters specified at initialisation.

        Parameters
        ----------
        seconds : float, optional
            During of the output waveform in seconds. The default is 5.
        n_harmonics : int, optional
            Number of harmonics to add to the output waveform. The default is 
            10.

        Returns
        -------
        waveform : ndarray
            The output signal.

        """
        
        sample_intervals = self.calculate_sample_intervals().astype(int)
        
        t = np.linspace(0, seconds, self.fs * seconds)
        waveform = np.zeros_like(t)
        
        total_samples = seconds * self.fs

        sample_intervals = np.insert(sample_intervals, 0, 0)
        remaining_samples = total_samples
        write_position = 0
        
        note_index = 0
        
        while(remaining_samples > sample_intervals[-1]):
            
            for i in range(sample_intervals.shape[0] - 1):
                    
                length = sample_intervals[i+1] - sample_intervals[i]
                pos1 = int(write_position + sample_intervals[i])
                pos2 = int(write_position + sample_intervals[i+1])
                chord = tf.generate_cluster_chord(self.notes[note_index])    
                waveform[pos1:pos2] = np.kaiser(length, 5) * tf.generate_n_sample_chord(chord, n_harmonics, length, self.fs)
                note_index += 1
                if note_index == len(self.notes):
                    note_index = 0
                
            remaining_samples -= self.samples_per_bar
            write_position += self.samples_per_bar
                
        return waveform
