import numpy as np

def grey_relational_coefficient(dist, dmin, dmax, rho=0.5):
    return (dmin + rho*dmax) / (dist + rho*dmax)

def gra_over_matrix(distance_matrix, rho=0.5):
    """
    distance_matrix: shape (N_demands, N_criteria)  每列已做“距离”化
    返回每个需求的整体关联度 P(Re0,Req)（式3-10）
    """
    dmin = np.min(distance_matrix)
    dmax = np.max(distance_matrix)
    coeff = grey_relational_coefficient(distance_matrix, dmin, dmax, rho)  # 逐元素
    scores = np.mean(coeff, axis=1)
    return scores
