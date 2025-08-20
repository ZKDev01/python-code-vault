""" 
Show property: there exists an n0 such that for all n (n0 < n) the following holds.
  sqrt(n) < log(n) < n < n*log(n) < n^c < x^n < n! < n^n

Comparison 1: 
  Linear, Quadratic, Exponential, Factorial 

Comparison 2:
  Logarithmic, Linear, Quasi-Linear
"""

import matplotlib.pyplot as plt 
import numpy as np 

# utils
def fact(xi):
  output = 1
  for i in range(1,int(xi)):
    output = output*i 
  return output

v_fact = np.vectorize(fact)

# style settings
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

n1 = np.linspace(1, 20 , 1000)
n2 = np.linspace(1, 100, 1000)

#region: comparison 1
ax1 = axes[0]

# functions: Linear, Quadratic, Exponential, Factorial
f_linear  = n1 
f_quad    = n1**2 
f_exp     = 2**n1 
f_fact    = v_fact(n1)

# plot
ax1.plot(n1, f_linear, 
  "blue", 
  linewidth=2, 
  label="Linear"
)
ax1.plot(n1, f_quad, 
  'red', 
  linewidth=2, 
  label="Quadratic"
)
ax1.plot(n1, f_exp, 
  'green', 
  linewidth=2, 
  label="Exponential"
)
ax1.plot(n1, f_fact, 
  "black",
  linewidth=2, 
  label="Factorial"
)

# settings

ax1.set_xlabel("x")
ax1.set_ylabel("f(x)")

ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 600)

#endregion

#region: comparison 2
ax2 = axes[1]

# funtions: Logarithmic, Linear, Quasi-Linear
f_log       = np.log(n2) 
f_linear    = n2 
f_q_linear  = n2 * np.log(n2)

# plot
ax2.plot(n2, f_log, 
  "blue",
  linewidth=2, 
  label="Logarithmic"
)
ax2.plot(n2, f_linear, 
  'red', 
  linewidth=2, 
  label="Linear"
)
ax2.plot(n2, f_q_linear, 
  'green', 
  linewidth=2, 
  label="Quasi-Linear"
)

# settings

ax2.set_xlabel("x")
ax2.set_ylabel("f(x)")

ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 600)

#endregion

plt.tight_layout()
plt.show()
