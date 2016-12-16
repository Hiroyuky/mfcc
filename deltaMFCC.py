import numpy as np

#-- miscellaneous utilities --#
def delta(X, axis=-1, order=1, pad=True):
    '''Compute delta features.

    :usage:
        >>> # Compute MFCC deltas, delta-deltas
        >>> mfccs       = librosa.feature.mfcc(y=y, sr=sr)
        >>> delta_mfcc  = librosa.feature.delta(mfccs)
        >>> delta2_mfcc = librosa.feature.delta(mfccs, order=2)

    :parameters:
      - X         : np.ndarray, shape=(d, T)
          the input data matrix (eg, spectrogram)

      - axis      : int
          the axis along which to compute deltas.
          Default is -1 (columns).

      - order     : int
          the order of the difference operator.
          1 for first derivative, 2 for second, etc.

      - pad       : bool
          set to True to pad the output matrix to the original size.

    :returns:
      - delta_X   : np.ndarray
          delta matrix of X.
    '''

    dx  = np.diff(X, n=order, axis=axis)

    if pad:
        padding         = [(0, 0)]  * X.ndim
        padding[axis]   = (order, 0)
        dx              = np.pad(dx, padding, mode='constant')

    return dx
