import numpy as np


def mag2db(mag):
    """
    Takes a linear amplitude and converts it to dB.

    Parameters
    ----------
    mag : float
        Linear magnitude

    Returns
    -------
    float
        The dB magnitude of the input value.

    """
    
    return 20 * np.log10(np.abs(mag))


def db2mag(db):
    """
    Takes a dB magnitude and converts it to linear.

    Parameters
    ----------
    db : float
        dB magnitude.

    Returns
    -------
    float
        The linear magnitude of the input value.

    """
    
    return 10**(db / 20.)
