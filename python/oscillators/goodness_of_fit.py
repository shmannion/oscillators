import numpy as np

def bhattacharyya_coefficient(p, q):
    """
    Compute the Bhattacharyya coefficient between two discrete distributions or vectors.

    Parameters
    ----------
    p, q : array-like
        Non-negative arrays of the same length.
        They don’t need to be normalized; the function will normalize them.

    Returns
    -------
    bc : float
        Bhattacharyya coefficient in [0, 1].
        1 = identical, 0 = no overlap.
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)

    # Check for valid input
    if np.any(p < 0) or np.any(q < 0):
        raise ValueError("Inputs must be non-negative.")

    # Normalize to sum to 1 (make them behave like distributions)
    p /= np.sum(p)
    q /= np.sum(q)

    # Compute Bhattacharyya coefficient
    bc = np.sum(np.sqrt(p * q))
    return bc

def bhattacharyya_distance(X1: np.ndarray, X2: np.ndarray) -> float:
    """
    Compute the Bhattacharyya distance between two multivariate Gaussian-distributed datasets.

    Parameters
    ----------
    X1 : np.ndarray
        n1 x m array (n1 samples, m variables)
    X2 : np.ndarray
        n2 x m array (n2 samples, m variables)

    Returns
    -------
    d : float
        The Bhattacharyya distance between the two distributions.
        Lower values indicate more overlap (better similarity).
    """
    # Ensure inputs are 2D
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)

    print(f'matrix shapes are {X1.shape} and {X2.shape}')
    # Check dimensions
    if X1.shape[1] != X2.shape[1]:
        raise ValueError("X1 and X2 must have the same number of columns (variables).")

    # Means and covariances
    mu1 = np.mean(X1, axis=0)
    mu2 = np.mean(X2, axis=0)
    C1 = np.cov(X1, rowvar=False)
    C2 = np.cov(X2, rowvar=False)

    # Average covariance
    C = 0.5 * (C1 + C2)

    # To avoid numerical issues with singular matrices
    try:
        C_inv = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        C_inv = np.linalg.pinv(C)

    # Mean difference term
    dmu = mu1 - mu2
    term1 = 0.125 * np.dot(np.dot(dmu.T, C_inv), dmu)

    # Determinant term
    det_C = np.linalg.det(C)
    det_C1 = np.linalg.det(C1)
    det_C2 = np.linalg.det(C2)

    # If determinants are near zero, use absolute values to avoid NaN
    if det_C <= 0 or det_C1 <= 0 or det_C2 <= 0:
        det_C = abs(det_C)
        det_C1 = abs(det_C1)
        det_C2 = abs(det_C2)

    term2 = 0.5 * np.log(det_C / np.sqrt(det_C1 * det_C2))

    d = float(term1 + term2)
    return d

def bhattacharyya_distance_hist(x1, x2, bins=50, range=None, eps=1e-10):
    """
    Compute the non-parametric Bhattacharyya distance between two 1D distributions.

    Parameters
    ----------
    x1, x2 : array-like
        1D numeric samples from each distribution.
    bins : int, optional
        Number of histogram bins.
    range : tuple, optional
        Range over which to compute histograms. Defaults to combined min/max of inputs.
    eps : float, optional
        Small value added to avoid log(0) or division by zero.

    Returns
    -------
    d : float
        Bhattacharyya distance between the two distributions (>= 0).
    """

    x1 = np.asarray(x1).ravel()
    x2 = np.asarray(x2).ravel()

    # Common histogram range
    if range is None:
        min_edge = min(x1.min(), x2.min())
        max_edge = max(x1.max(), x2.max())
        range = (min_edge, max_edge)

    # Compute normalized histograms (probability densities)
    p_hist, edges = np.histogram(x1, bins=bins, range=range, density=True)
    q_hist, _     = np.histogram(x2, bins=bins, range=range, density=True)

    # Normalize to sum to 1 (probability mass)
    p_hist /= (p_hist.sum() + eps)
    q_hist /= (q_hist.sum() + eps)

    # Bhattacharyya coefficient
    bc = np.sum(np.sqrt(p_hist * q_hist))

    # Bhattacharyya distance
    d = -np.log(bc + eps)
    return float(d)

