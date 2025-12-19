
import numpy as np
import matplotlib.pyplot as plt
import os

# Set up the box
L = 1.0
x = np.linspace(0, L, 1000)

# Define the two wavefunctions
psi_1 = np.sqrt(2) * np.sin(1 * np.pi * x / L)  # n=1
psi_2 = np.sqrt(2) * np.sin(2 * np.pi * x / L)  # n=2

# Superposition (just add them!)
psi_super = (psi_1 + psi_2) / np.sqrt(2)

# Probability densities
prob_1 = psi_1**2
prob_2 = psi_2**2
prob_super = psi_super**2

# Create detailed visualization
fig = plt.figure(figsize=(14, 10))

# Top row: Individual wavefunctions
ax1 = plt.subplot(3, 2, 1)
ax1.plot(x, psi_1, 'b-', linewidth=2)
ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax1.fill_between(x, 0, psi_1, alpha=0.3, color='blue')
ax1.set_ylabel('ψ₁(x)')
ax1.set_title('State |n=1⟩ (Ground State)')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, 1])

ax2 = plt.subplot(3, 2, 2)
ax2.plot(x, psi_2, 'r-', linewidth=2)
ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax2.fill_between(x, 0, psi_2, where=(psi_2>0), alpha=0.3, color='red', interpolate=True)
ax2.fill_between(x, 0, psi_2, where=(psi_2<0), alpha=0.3, color='blue', interpolate=True)
ax2.set_ylabel('ψ₂(x)')
ax2.set_title('State |n=2⟩ (First Excited)')
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, 1])

# Middle row: Adding the wavefunctions
ax3 = plt.subplot(3, 2, 3)
ax3.plot(x, psi_1, 'b--', linewidth=1.5, alpha=0.6, label='ψ₁')
ax3.plot(x, psi_2, 'r--', linewidth=1.5, alpha=0.6, label='ψ₂')
ax3.plot(x, psi_super, 'purple', linewidth=2.5, label='ψ₁ + ψ₂')
ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax3.set_ylabel('Wavefunction')
ax3.set_title('Adding the Wavefunctions')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim([0, 1])

# Add annotations at key points
ax3.annotate('Constructive\ninterference', xy=(0.25, psi_super[250]), 
            xytext=(0.25, 2.5), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax3.annotate('Destructive\ninterference', xy=(0.75, psi_super[750]), 
            xytext=(0.75, 2.5), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

# Detailed view at x=0.25 (left side)
ax4 = plt.subplot(3, 2, 4)
detail_range = (x > 0.2) & (x < 0.3)
ax4.plot(x[detail_range], psi_1[detail_range], 'b-', linewidth=2, label='ψ₁ (positive)')
ax4.plot(x[detail_range], psi_2[detail_range], 'r-', linewidth=2, label='ψ₂ (positive)')
ax4.plot(x[detail_range], psi_super[detail_range], 'purple', linewidth=3, label='Sum (LARGER)')
ax4.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax4.set_ylabel('Wavefunction')
ax4.set_xlabel('Position x')
ax4.set_title('At x=0.25: BOTH POSITIVE → Add up!')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Detailed view at x=0.75 (right side)
ax5 = plt.subplot(3, 2, 5)
detail_range = (x > 0.7) & (x < 0.8)
ax5.plot(x[detail_range], psi_1[detail_range], 'b-', linewidth=2, label='ψ₁ (positive)')
ax5.plot(x[detail_range], psi_2[detail_range], 'r-', linewidth=2, label='ψ₂ (negative)')
ax5.plot(x[detail_range], psi_super[detail_range], 'purple', linewidth=3, label='Sum (smaller)')
ax5.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
ax5.set_ylabel('Wavefunction')
ax5.set_xlabel('Position x')
ax5.set_title('At x=0.75: OPPOSITE SIGNS → Cancel out!')
ax5.legend()
ax5.grid(True, alpha=0.3)

# Bottom: Final probability density
ax6 = plt.subplot(3, 2, 6)
ax6.plot(x, prob_super, 'purple', linewidth=2.5)
ax6.fill_between(x, 0, prob_super, alpha=0.3, color='purple')
ax6.set_ylabel('|ψ(x)|²')
ax6.set_xlabel('Position x')
ax6.set_title('Final Probability Density: LEFT > RIGHT!')
ax6.grid(True, alpha=0.3)
ax6.set_xlim([0, 1])

# Mark peak locations
left_peak_idx = 250  # around x=0.25
right_peak_idx = 750  # around x=0.75
ax6.plot(x[left_peak_idx], prob_super[left_peak_idx], 'go', markersize=10, label=f'Left peak: {prob_super[left_peak_idx]:.2f}')
ax6.plot(x[right_peak_idx], prob_super[right_peak_idx], 'ro', markersize=10, label=f'Right peak: {prob_super[right_peak_idx]:.2f}')
ax6.legend()

plt.tight_layout()

output_dir = './qm_plots_simple'
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, 'superposition_explanation.png')
plt.savefig(filename, dpi=150, bbox_inches='tight')
print(f"✓ Detailed explanation saved: {filename}")
plt.close()
