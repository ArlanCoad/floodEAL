#EAL(Expected Annual Loss) Calculator for parents home flood risk
#Needs: Expected Annual Damages

import math
from typing import List, Tuple

#houses replacement value incase of complete damge
replacement_value =  float(733072)

"""
Important Data

Basement floor elevation: 110.5 ft 
$733,072 is houses estimated value based on Redfin. Denoted as replacement_value

Overall Flooding Hazard is High according to NC Flood Risk Information System(FRIS).
Expected Annual Loss($) = 0. Why? Hazard is about location risk, not guaranteed building damage.
House is located near flood plain though is not at risk of flooding. :)
"""

#(annualProbability, depth_ft);
rows = [
    (0.10, 0.0),
    (0.04, 0.0),
    (0.02, -14.9),
    (0.01, -13.7), # 1% event
    (0.002, -10.1), # 0.2% a.k.a 500-year flood
]

rows.sort(reverse=True)

for p, depth in rows:
    print("Probability: ", p, "Depth: ", depth)

#Simple Damage Ratios Mark 1
#Damage ratios are assumptioms
"""
def damageRatio(depth_ft: float) -> float:
    if depth_ft <= 0:
        return 0.0 
    elif depth_ft <= 1:
        return 0.05
    elif depth_ft <= 3:
        return 0.15
    elif depth_ft <= 6:
        return 0.35
    else:
        return 0.6
"""

#logistic curve mark 2
"""
K denotes steepness. K is greater -> greater slope.
logistic function 
f(x) = 1 / [1 + e^( -k ( x-m ))]
m(midpoint) is where damage reaches 50% of maximum damage
m = 4 ft for typical residential housing
"""
def damageRatio(depth_ft):
    if depth_ft <= 0:
        return 0.0
    
    k = 0.8
    midpoint = 4
    #f(x) = 1 / [1 + e^( -k ( x-m ))]
    ratio = 1 / (1 + max.exp(-k * (depth_ft - midpoint)))
    return min(ratio, 1.0)
    
def compute_eal(rows: List[Tuple[float, float]], replacement_value: float) -> float:
    rows = sorted(rows, key=lambda x: x[0], reverse=True) #exceedance probabilities in descending order 0.10, 0.04, ...

    eal = 0.0 #initialize eal to 0
    
    for i in range(len(rows)): #len returns # of items in rows
        p_i, d_i = rows[i] #p_i = annualProbability, d_i = depth
        p_next = rows[i + 1][0] if i + 1 < len(rows) else 0.0

        # dp(probability of severity band) = P(Depth >= d_i) - P(Depth >= d_(i+1))
        dp = p_i - p_next
        # safety check
        if dp < 0:
            raise ValueError("Probabilites not in descending order.")
        
        #converting dept into dollar lose value
        loss_i = replacement_value * damageRatio(d_i)
        #eal = summation(dp * loss in band)
        eal += dp * loss_i
    
    return eal

eal = compute_eal(rows, replacement_value)
print("Expected Annual Loss($): ", round(eal, 2))

