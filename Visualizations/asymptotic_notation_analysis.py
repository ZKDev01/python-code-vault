import matplotlib.pyplot as plt
import numpy as np

# style settings
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(1, 3, figsize=(18, 8))
fig.suptitle(r'Asymptotic Notations: Big O, $\Omega$ y $\Theta$', fontsize=16, fontweight='bold')

n = np.linspace(1, 20, 1000)

#region: BIG O
ax1 = axes[0]

Tn_bigo = n**2 + n + 1
fn_bigo = n**2
c = 2  

# plot functions
ax1.plot(n, Tn_bigo, 'b-', linewidth=2, label=r'$T(n) = n^2 + n + 2$')
ax1.plot(n, c * fn_bigo, 'r--', linewidth=2, label=fr'$cf(n) = {c}n^2$')

ax1.set_title(r'Big O $(O)$: $T(n) \in O(f(n)) | T(n) \leq cf(n)$', fontweight='bold')
ax1.set_xlabel('n (input size)')
ax1.set_ylabel('Time/Complexity')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 500)

#endregion

#region OMEGA
ax2 = axes[1]

Tn_omega = n**2 + 5*n + 10
fn_omega = n**2
c_omega = 0.5  

ax2.plot(n, Tn_omega, 'b-', linewidth=2, label=r'$T(n) = n^2 + 5n + 10$')
ax2.plot(n, c_omega * fn_omega, 'orange', linestyle='--', linewidth=2, label=fr'$c \cdot f(n) = {c_omega}n^2$')

ax2.set_title(r'Omega ($\Omega$): $T(n) \in \Omega(f(n)) | T(n) \leq c \cdot f(n)$', fontweight='bold')
ax2.set_xlabel('n (input size)')
ax2.set_ylabel('Time/Complexity')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 500)

#endregion

#region THETA
ax3 = axes[2]

Tn_theta = 2*n**2 + 3*n + 1
fn_theta = n**2
c1_theta = 1.5  # lower constant
c2_theta = 3    # upper constant

ax3.plot(n, Tn_theta, 'b-', linewidth=3, label=r'$T(n) = 2n^2 + 3n + 1$')
ax3.plot(n, c1_theta * fn_theta, 'green', linestyle='--', linewidth=2, label=fr'$c_1 \cdot f(n) = {c1_theta}n^2$ (lower const.)')
ax3.plot(n, c2_theta * fn_theta, 'red', linestyle='--', linewidth=2, label=fr'$c_2 \cdot f(n) = {c2_theta}n^2$ (upper const.)')

ax3.set_title(r'Theta ($\Theta$): $T(n) \in \Theta(f(n)) | c_1 \cdot f(n) \leq T(n) \leq c_2 \cdot f(n)$', fontweight='bold')
ax3.set_xlabel('n (input size)')
ax3.set_ylabel('Time/Complexity')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 600)

#endregion

plt.tight_layout()
plt.show()
