"""
Functions for manipulating input piano keys and generating corresponding
waveforms
"""

import numpy as np

def get_frequency_from_note(note_n):
    """
    Give a note on the piano, returns the frequency in Hz of that note.

    Parameters
    ----------
    note_n : int
        Numerical representation of a piano key.

    Returns
    -------
    float
        The frequency in Hz of tbe note.

    """
    
    return ((2)**(1/12))**(note_n-49) * 440


def generate_n_sample_sine(note, n_samples, sample_rate=44100):
    """
    Generates a sine wave of n samples for the input note.
    
    Parameters
    ----------
    note : int
        Numerical representation of a piano key.
    n_samples : int
        Number of samples to generate.
    sample_rate : int, optional
        The sample rate of the output sine wav. The default is 44100.

    Returns
    -------
    ndarray
        An array containing the generated sine wave.

    """
    frequency = get_frequency_from_note(note)
    
    samples = np.arange(0, n_samples, 1)
    
    t = samples * (1/sample_rate)
    
    return np.sin(2 * np.pi * frequency * t)


def generate_n_sample_sine_with_harmonics(note, n_harmonics, n_samples, 
                                          sample_rate=44100):
    """
    Generates a sine wave of n_samples with n_harmonics present in the
    waveform.
    
    Parameters
    ----------
    note : int
        Numerical representation of a piano key.
    n_harmonics : int
        Number of harmonics present in the waveform.
    n_samples : int
        Number of samples to generate.
    sample_rate : int, optional
        The sample rate of the output sine wav. The default is 44100.

    Returns
    -------
    output : ndarray
        An array containing the generated signal.

    """
    
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
    """
    Generates a cluster chord given an input note.

    Parameters
    ----------
    note : int
        Numerical representation of a piano key.

    Returns
    -------
    ndarray
        An array containing the notes present in the chord.

    """
    
    return np.array([note, note + 4, note + 7, note + 9])


def generate_n_sample_chord(chord, n_harmonics, n_samples, sample_rate=44100):
    """
    Generates a waveform of n samples for a given chord.

    Parameters
    ----------
    chord : ndarray
        An array containing the notes of the chord.
    n_harmonics : int
        Number of harmonics present in the waveform.
    n_samples : int
        Number of samples to generate.
    sample_rate : int, optional
        The sample rate of the output sine wav. The default is 44100.

    Returns
    -------
    output : ndarray
        An array containing the generated signal.

    """
    
    output = np.zeros(n_samples)
    
    for i in range(chord.shape[0]):
        output += generate_n_sample_sine_with_harmonics(chord[i], n_harmonics, 
                                                        n_samples, sample_rate)
    
    return output