
import numpy as np
from math import sin, cos, tan, radians, atan2, degrees
from scipy.optimize import minimize_scalar

def oms(df):
    """
    Computes the Factor of Safety (FS) using the Ordinary Method of Slices (OMS).
    This method works on circular failure surfaces only.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data with columns:
            - 'alpha': base angle (degrees)
            - 'w': total slice weight
            - 'c': cohesion
            - 'phi': friction angle (degrees)
            - 'u': pore pressure
            - 'dl': base length
            - 'shear_reinf' (optional): reinforcement force opposing sliding (FL)
            - 'normal_reinf' (optional): reinforcement force contributing to base normal force (FT)

    Returns:
        tuple:
            - float: Computed Factor of Safety (FS)
            - np.ndarray: Normal force on the base of each slice
    """

    alpha_rad = np.radians(df['alpha'])

    cos_alpha = np.cos(alpha_rad)
    sin_alpha = np.sin(alpha_rad)
    cos2_alpha = cos_alpha ** 2

    W = df['w'].values
    shear_reinf = df.get('shear_reinf', 0).values
    normal_reinf = df.get('normal_reinf', 0).values
    c = df['c'].values
    phi = np.radians(df['phi']).values
    u = df['u'].values
    dl = df['dl'].values

    N = W * cos_alpha - u * dl * cos2_alpha + normal_reinf
    numerator = c * dl + N * np.tan(phi)
    denominator = W * sin_alpha - shear_reinf
    FS = numerator.sum() / denominator.sum() if denominator.sum() != 0 else float('inf')

    return FS, N


def bishop(df, tol=1e-6, max_iter=100):
    """
    Computes the Factor of Safety (FS) using Bishop's Simplified Method.
    This method works on circular failure surfaces only.
    It iterates on the factor of safety until convergence is achieved.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data with necessary columns.
        tol (float, optional): Convergence tolerance. Default is 1e-6.
        max_iter (int, optional): Maximum number of iterations. Default is 100.

    Returns:
        tuple:
            - float: Computed Factor of Safety (FS)
            - np.ndarray: Normal force on the base of each slice
            - bool: Whether the solution converged
    """

    alpha_rad = np.radians(df['alpha'])
    cos_alpha = np.cos(alpha_rad)
    sin_alpha = np.sin(alpha_rad)
    cos2_alpha = cos_alpha**2
    tan_phi = np.tan(np.radians(df['phi']))

    W = df['w']
    shear_reinf = df.get('shear_reinf', 0)
    normal_reinf = df.get('normal_reinf', 0)
    c = df['c']
    dl = df['dl']
    u = df['u']

    # Right-hand side: sum of W * sin(alpha)
    denominator = (W * sin_alpha - shear_reinf).sum()

    # Start iteration with an initial guess
    converge = False
    F_guess = 1.0
    N = W * cos_alpha - u * dl * cos2_alpha + normal_reinf
    num = c * dl + N * tan_phi
    for _ in range(max_iter):
        denom = cos_alpha + (sin_alpha * tan_phi) / F_guess
        terms = num / denom
        F_calc = terms.sum() / denominator
        if abs(F_calc - F_guess) < tol:
            converge = True
            break
        F_guess = F_calc

    return F_calc, N, converge



def spencer(df, tol=1e-6, max_iter=100):
    """
    Computes the Factor of Safety (FS) using Spencer's Method.
    This version works on circular failure surfaces only. For non-circular surfaces, use
    `spencer_moment` instead.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data.
        tol (float, optional): Convergence tolerance. Default is 1e-6.
        max_iter (int, optional): Maximum number of iterations. Default is 100.

    Returns:
        tuple:
            - float: Computed Factor of Safety (FS)
            - float: Inter-slice force inclination angle (degrees)
    """

    alpha_rad = np.radians(df['alpha'])
    phi_rad = np.radians(df['phi'])
    tan_phi = np.tan(phi_rad)

    W = df['w'].values
    shear_reinf = df.get('shear_reinf', 0)
    normal_reinf = df.get('normal_reinf', 0)
    c = df['c'].values
    dl = df['dl'].values
    u = df['u'].values

    sin_alpha = np.sin(alpha_rad)
    cos_alpha = np.cos(alpha_rad)
    cos2_alpha = cos_alpha ** 2

    # Initial guesses
    F = 1.0
    beta = 0.0  # in radians

    for _ in range(max_iter):
        sin_beta = np.sin(beta)
        cos_beta = np.cos(beta)

        # Compute resisting force per slice
        denom = cos_alpha * cos_beta + sin_alpha * sin_beta * np.tan(phi_rad)
        effective_W = W + normal_reinf / cos_alpha  # distribute normal reinforcement as an equivalent weight
        num = c * dl * cos_beta + (effective_W - u * dl) * (cos_alpha * cos_beta - sin_alpha * sin_beta) * tan_phi
        num = c * dl * cos_beta + (W - u * dl) * (cos_alpha * cos_beta - sin_alpha * sin_beta) * np.tan(phi_rad)
        F_new = num.sum() / (W * sin_alpha - shear_reinf).sum()

        # Update beta using ratio of residual horizontal and vertical forces
        sin_beta_new = (W * sin_alpha - num / F_new * sin_alpha * tan_phi) / W
        beta_new = np.arcsin(np.clip(sin_beta_new.mean(), -1.0, 1.0))  # averaged beta

        if abs(F_new - F) < tol and abs(beta_new - beta) < tol:
            return F_new, degrees(beta_new)

        F = F_new
        beta = beta_new

    return F, degrees(beta)

def spencer_moment(df, beta_bounds=(-60, 60), tol=1e-6, max_iter=100):
    """
    Implements Spencer's Method (UTEXASED-style):
    - Sweeps beta
    - Solves FS from force equilibrium and FS from moment equilibrium independently
    - Returns beta where FS_force = FS_moment

    Parameters:
        df (pd.DataFrame): Slice data with keys:
            'alpha', 'phi', 'c', 'w', 'u', 'dl', 'x_c', 'y_cb'
        beta_bounds (tuple): Beta search range in degrees
        tol (float): Convergence tolerance
        max_iter (int): Max iterations per FS solve

    Returns:
        float: Factor of Safety
        float: Beta (degrees)
    """
    alpha = np.radians(df['alpha'])
    phi = np.radians(df['phi'])
    tan_phi = np.tan(phi)

    c = df['c'].values
    dl = df['dl'].values
    w = df['w'].values
    u = df['u'].values
    x_c = df['x_c'].values
    y_cb = df['y_cb'].values

    shear_reinf = df.get('shear_reinf', 0).values
    normal_reinf = df.get('normal_reinf', 0).values

    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    cos2_alpha = cos_alpha ** 2

    def fs_force(beta_rad):
        sin_beta = np.sin(beta_rad)
        cos_beta = np.cos(beta_rad)
        F = 1.0
        for _ in range(max_iter):
            N = w * cos_alpha - u * dl * cos2_alpha + normal_reinf
            denom = cos_alpha * cos_beta + sin_alpha * sin_beta * tan_phi
            num = c * dl * cos_beta + N * (cos_alpha * cos_beta - sin_alpha * sin_beta) * tan_phi
            T = w * sin_alpha - shear_reinf
            F_new = num.sum() / T.sum()
            if abs(F_new - F) < tol:
                break
            F = F_new
        return F

    def fs_moment(beta_rad):
        F = 1.0
        for _ in range(max_iter):
            N = w * cos_alpha - u * dl * cos2_alpha + normal_reinf
            S = c * dl + N * tan_phi / F
            M_resist = (S * y_cb).sum()
            M_drive = (w * x_c).sum()
            F_new = M_resist / M_drive
            if abs(F_new - F) < tol:
                break
            F = F_new
        return F

    def fs_difference(beta_deg):
        beta_rad = radians(beta_deg)
        return abs(fs_force(beta_rad) - fs_moment(beta_rad))

    result = minimize_scalar(fs_difference, bounds=beta_bounds, method='bounded', options={'xatol': tol})
    beta_deg = result.x
    beta_rad = radians(beta_deg)
    FS_final = fs_force(beta_rad)
    return FS_final, beta_deg

def janbu_simple(df, tol=1e-6, max_iter=100):
    """
    Computes the Factor of Safety (FS) using Janbu's Simplified Method.
    This method is based on force equilibrium and is valid for both circular and non-circular failure surfaces.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data.
        tol (float, optional): Convergence tolerance. Default is 1e-6.
        max_iter (int, optional): Maximum number of iterations. Default is 100.

    Returns:
        float: Computed Factor of Safety (FS)
    """

    alpha_rad = np.radians(df['alpha'])
    phi_rad = np.radians(df['phi'])
    tan_phi = np.tan(phi_rad)

    W = df['w']
    shear_reinf = df.get('shear_reinf', 0)
    normal_reinf = df.get('normal_reinf', 0)
    c = df['c'].values
    dl = df['dl'].values
    u = df['u'].values

    sin_alpha = np.sin(alpha_rad)
    cos_alpha = np.cos(alpha_rad)

    F = 1.0  # initial guess

    for _ in range(max_iter):
        N = W * cos_alpha + normal_reinf
        S = c * dl + (N - u * dl) * tan_phi / F
        T = W * sin_alpha - shear_reinf

        F_new = S.sum() / T.sum()

        if abs(F_new - F) < tol:
            return F_new

        F = F_new

    return F


def janbu_corrected(df, tol=1e-6, max_iter=100):
    """
    Computes the Factor of Safety (FS) using Janbu's Corrected Method.
    This method is based on force equilibrium and is valid for both circular and non-circular failure surfaces.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data.
        tol (float, optional): Convergence tolerance. Default is 1e-6.
        max_iter (int, optional): Maximum number of iterations. Default is 100.

    Returns:
        tuple:
            - float: Computed Factor of Safety (FS)
            - float: Horizontal force ratio (lambda)
            - bool: Whether the solution converged
    """

    alpha_rad = np.radians(df['alpha'])
    phi_rad = np.radians(df['phi'])
    tan_phi = np.tan(phi_rad)

    W = df['w']
    shear_reinf = df.get('shear_reinf', 0)
    normal_reinf = df.get('normal_reinf', 0)
    c = df['c'].values
    dl = df['dl'].values
    u = df['u'].values

    sin_alpha = np.sin(alpha_rad)
    cos_alpha = np.cos(alpha_rad)

    F = 1.0
    lambda_ = 0.0
    converged = False

    for _ in range(max_iter):
        m = 1 + lambda_ * tan_phi / F

        N = W * cos_alpha + normal_reinf
        S = c * dl + (N - u * dl) * tan_phi / F
        R = S / m
        T = W * sin_alpha - shear_reinf

        F_new = R.sum() / T.sum()
        lambda_new = (R * sin_alpha).sum() / (R * cos_alpha).sum()

        if abs(F_new - F) < tol and abs(lambda_new - lambda_) < tol:
            converged = True
            break

        F = F_new
        lambda_ = lambda_new

    return F, lambda_, converged


def morgenstern_price(df, function=lambda x: 1.0, tol=1e-6, max_iter=100):
    """
    Computes the Factor of Safety (FS) using the Morgenstern-Price Method.
    This method is valid for both circular and non-circular failure surfaces.

    Parameters:
        df (pd.DataFrame): DataFrame containing slice data.
        function (callable, optional): A callable defining the inter-slice force function ψ(x),
            where x is normalized from 0 to 1 across slices. Default is constant function (1.0).
        tol (float, optional): Convergence tolerance. Default is 1e-6.
        max_iter (int, optional): Maximum number of iterations. Default is 100.

    Returns:
        tuple:
            - float: Computed Factor of Safety (FS)
            - float: Inter-slice force ratio (lambda)
            - bool: Whether the solution converged
    """
    alpha_rad = np.radians(df['alpha'])
    phi_rad = np.radians(df['phi'])
    tan_phi = np.tan(phi_rad)

    W = df['w']
    shear_reinf = df.get('shear_reinf', 0)
    normal_reinf = df.get('normal_reinf', 0)
    c = df['c'].values
    dl = df['dl'].values
    u = df['u'].values

    sin_alpha = np.sin(alpha_rad)
    cos_alpha = np.cos(alpha_rad)

    # Inter-slice function shape (normalized to [0, 1])
    n = len(df)
    x_norm = np.linspace(0, 1, n)
    psi = np.array([function(xi) for xi in x_norm])

    F = 1.0
    lam = 0.0
    converged = False

    for _ in range(max_iter):
        m = 1 + lam * psi * tan_phi / F

        N = W * cos_alpha + normal_reinf
        S = c * dl + (N - u * dl) * tan_phi / F
        R = S / m
        T = W * sin_alpha - shear_reinf

        F_new = R.sum() / T.sum()
        num = (R * psi * sin_alpha).sum()
        den = (R * psi * cos_alpha).sum()
        lam_new = num / den if den != 0 else 0.0

        if abs(F_new - F) < tol and abs(lam_new - lam) < tol:
            converged = True
            break

        F = F_new
        lam = lam_new

    return F, lam, converged