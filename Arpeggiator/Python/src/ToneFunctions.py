import numpy as np

def get_frequency_from_note(note_n):
    """
    Give a note on the piano, returns the frequency in Hz of that note.
    """
    
    return ((2)**(1/12))**(note_n-49) * 440


def generate_n_sample_sine(frequency, n_samples, sample_rate=44100):
    
    samples = np.arange(0, n_samples, 1)
    
    t = samples * (1/sample_rate)
    
    return np.sin(2 * np.pi * frequency * t)


def generate_n_sample_sine_with_harmonics(note, n_harmonics, n_samples, sample_rate=44100):
    
    frequency = get_frequency_from_note(note)
    
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


def generate_cluster_chord(note):
    
    return np.array([note, note + 4, note + 7, note + 9])


def generate_n_sample_chord(note, n_harmonics, n_samples, sample_rate=44100):
    
    chord = generate_cluster_chord(note)    
    
    output = np.zeros(n_samples)
    
    for i in range(chord.shape[0]):
        output += generate_n_sample_sine_with_harmonics(chord[i], n_harmonics, n_samples, sample_rate)
    
    return output