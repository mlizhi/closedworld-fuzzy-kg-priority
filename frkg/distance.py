import numpy as np

# 符合式(3-5)
def d_symbolic(mu_alpha, mu_beta_x, mu_beta_y, same: bool):
    if same: return 0.0
    return 1 - (mu_alpha * mu_beta_x * mu_beta_y)

# 式(3-6) 需要提供全局 min/max
def d_real(mu_alpha, mu_beta_x, mu_beta_y, vx, vy, vmin, vmax):
    if vmax == vmin: return 0.0
    return (mu_alpha * mu_beta_x * mu_beta_y) * (abs(vx - vy) / (vmax - vmin))

# 式(3-7)
def d_semantic(mu_alpha, mu_beta_x, mu_beta_y, pos_x, pos_y, tau):
    return (mu_alpha * mu_beta_x * mu_beta_y) * (abs(pos_x - pos_y) / (2*tau + 1))

# 式(3-8)
def d_interval(mu_alpha, mu_beta_x, mu_beta_y, x_low, x_up, y_low, y_up):
    return (mu_alpha * mu_beta_x * mu_beta_y) * (np.sqrt(2)/2.0) * np.sqrt((x_up-y_up)**2 + (x_low-y_low)**2)

# 式(3-9)
def d_mixed(distances):
    """distances: list of scalar d(v(x),v(y)) from different attributes a∈A"""
    if not distances: return 0.0
    return np.sqrt((1/len(distances)) * np.sum(np.square(distances)))
