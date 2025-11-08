import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# Define the problem parameters
E0 = 1.0  # Energy eigenvalue for |0⟩ (we can set this to any non-zero value)
E1 = 0.0  # Energy eigenvalue for |1⟩

print("=" * 70)
print("TWO-LEVEL QUANTUM SYSTEM ANALYSIS")
print("=" * 70)
print(f"\nEnergy eigenvalues: E₀ = {E0}, E₁ = {E1}")

# Part (a): Determine α and normalization constants
print("\n" + "=" * 70)
print("PART (a): Determining α and normalization constants")
print("=" * 70)

# Position eigenstates in energy basis:
# |x₀⟩ = c₀(|0⟩ + |1⟩)
# |x₁⟩ = c₁(|0⟩ + α|1⟩)

# For position operator X to be Hermitian, we need X|x₀⟩ = x₀|x₀⟩ and X|x₁⟩ = x₁|x₁⟩
# Also, position eigenstates must be orthogonal: ⟨x₀|x₁⟩ = 0

# Orthogonality condition: ⟨x₀|x₁⟩ = c₀*c₁*(1 + α) = 0
# Since c₀, c₁ ≠ 0 (for non-trivial states), we need: 1 + α = 0
alpha = -1.0
print(f"\nFrom orthogonality condition ⟨x₀|x₁⟩ = 0:")
print(f"α = {alpha}")

# Normalization of |x₀⟩: |c₀|²(1 + 1) = 1
c0_squared = 1/2
c0 = np.sqrt(c0_squared)
print(f"\nNormalization of |x₀⟩:")
print(f"|c₀|² = {c0_squared}")
print(f"c₀ = {c0:.4f} (choosing positive real value)")

# Normalization of |x₁⟩: |c₁|²(1 + |α|²) = 1
c1_squared = 1/(1 + abs(alpha)**2)
c1 = np.sqrt(c1_squared)
print(f"\nNormalization of |x₁⟩:")
print(f"|c₁|² = {c1_squared}")
print(f"c₁ = {c1:.4f} (choosing positive real value)")

# Verify orthonormality
print("\nVerification:")
print(f"⟨x₀|x₀⟩ = {2*c0_squared:.4f} ✓")
print(f"⟨x₁|x₁⟩ = {c1_squared*(1 + alpha**2):.4f} ✓")
print(f"⟨x₀|x₁⟩ = {c0*c1*(1 + alpha):.4f} ✓")

# Part (b): Matrices for Hamiltonian and position operator
print("\n" + "=" * 70)
print("PART (b): Hamiltonian and Position operator matrices")
print("=" * 70)

# In energy representation, H is diagonal
H_energy = np.array([[E0, 0],
                     [0, E1]])
print("\nHamiltonian in energy representation:")
print(H_energy)

# Position operator eigenvalues (we can choose these)
# Let's set x₀ = 1 and x₁ = -1 for concreteness
x0 = 1.0
x1 = -1.0
print(f"\nPosition eigenvalues: x₀ = {x0}, x₁ = {x1}")

# Position eigenstates as column vectors in energy basis
ket_x0 = c0 * np.array([[1], [1]])
ket_x1 = c1 * np.array([[1], [alpha]])

# Position operator in energy representation
# X = x₀|x₀⟩⟨x₀| + x₁|x₁⟩⟨x₁|
X_energy = x0 * (ket_x0 @ ket_x0.conj().T) + x1 * (ket_x1 @ ket_x1.conj().T)
print("\nPosition operator X in energy representation:")
print(X_energy)

# Verify X is Hermitian
print("\nVerification that X is Hermitian:")
print(f"X = X†: {np.allclose(X_energy, X_energy.conj().T)} ✓")

# Verify eigenvalues and eigenvectors
eigenvalues_X, eigenvectors_X = np.linalg.eigh(X_energy)
print(f"\nEigenvalues of X: {eigenvalues_X}")
print(f"Expected: [{x1}, {x0}]")
print(f"Match: {np.allclose(sorted(eigenvalues_X), sorted([x0, x1]))} ✓")

# Part (c): Time evolution of position expectation value
print("\n" + "=" * 70)
print("PART (c): Time evolution of ⟨X⟩(t)")
print("=" * 70)

# Initial state at t=0 is |x₀⟩
# Time evolution: |ψ(t)⟩ = e^(-iHt/ℏ)|ψ(0)⟩
# We'll use ℏ = 1 for simplicity

# Initial state in energy basis
psi_0 = ket_x0  # |ψ(0)⟩ = |x₀⟩

# Time array
hbar = 1.0
t_max = 20.0
t_array = np.linspace(0, t_max, 500)

# Calculate ⟨X⟩(t)
X_expectation = np.zeros_like(t_array)

for i, t in enumerate(t_array):
    # Time evolution operator
    U_t = expm(-1j * H_energy * t / hbar)
    
    # Evolved state
    psi_t = U_t @ psi_0
    
    # Expectation value
    X_expectation[i] = np.real((psi_t.conj().T @ X_energy @ psi_t)[0, 0])

print(f"\nInitial expectation value ⟨X⟩(0) = {X_expectation[0]:.4f}")
print(f"Expected: x₀ = {x0}")

# Analytical expression
# |ψ(t)⟩ = c₀(e^(-iE₀t/ℏ)|0⟩ + e^(-iE₁t/ℏ)|1⟩)
# ⟨X⟩(t) = can be computed analytically
omega = (E0 - E1) / hbar
print(f"\nAngular frequency ω = (E₀ - E₁)/ℏ = {omega:.4f}")

# Analytical formula
X_analytical = np.zeros_like(t_array)
for i, t in enumerate(t_array):
    X_analytical[i] = c0**2 * (x0 + x1) + c0**2 * (x0 - x1) * np.cos(omega * t)

print("\nAnalytical formula:")
print(f"⟨X⟩(t) = {c0**2 * (x0 + x1):.4f} + {c0**2 * (x0 - x1):.4f} cos(ωt)")

# Part (d): Standard deviation
print("\n" + "=" * 70)
print("PART (d): Standard deviation σₓ(t)")
print("=" * 70)

# σₓ² = ⟨X²⟩ - ⟨X⟩²
X_squared = X_energy @ X_energy

X_squared_expectation = np.zeros_like(t_array)
sigma_x = np.zeros_like(t_array)

for i, t in enumerate(t_array):
    # Time evolution operator
    U_t = expm(-1j * H_energy * t / hbar)
    
    # Evolved state
    psi_t = U_t @ psi_0
    
    # ⟨X²⟩
    X_squared_expectation[i] = np.real((psi_t.conj().T @ X_squared @ psi_t)[0, 0])
    
    # Standard deviation
    sigma_x[i] = np.sqrt(X_squared_expectation[i] - X_expectation[i]**2)

print(f"\nInitial standard deviation σₓ(0) = {sigma_x[0]:.4f}")
print(f"Final standard deviation σₓ({t_max}) = {sigma_x[-1]:.4f}")

# Analytical expression for ⟨X²⟩
X2_analytical = np.zeros_like(t_array)
for i, t in enumerate(t_array):
    X2_analytical[i] = c0**2 * (x0**2 + x1**2) + c0**2 * (x0**2 - x1**2) * np.cos(omega * t)

sigma_x_analytical = np.sqrt(X2_analytical - X_analytical**2)

print(f"\nσₓ(t) oscillates between {sigma_x.min():.4f} and {sigma_x.max():.4f}")

# Visualization
print("\n" + "=" * 70)
print("GENERATING PLOTS")
print("=" * 70)

fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Plot (c): Position expectation value
ax1 = axes[0]
ax1.plot(t_array, X_expectation, 'b-', linewidth=2, label='Numerical')
ax1.plot(t_array, X_analytical, 'r--', linewidth=1.5, alpha=0.7, label='Analytical')
ax1.axhline(y=x0, color='gray', linestyle=':', alpha=0.5, label=f'x₀ = {x0}')
ax1.axhline(y=x1, color='gray', linestyle=':', alpha=0.5, label=f'x₁ = {x1}')
ax1.set_xlabel('Time (ℏ/E₀)', fontsize=12)
ax1.set_ylabel('⟨X⟩(t)', fontsize=12)
ax1.set_title('Position Expectation Value vs Time', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Plot (d): Standard deviation
ax2 = axes[1]
ax2.plot(t_array, sigma_x, 'g-', linewidth=2, label='Numerical')
ax2.plot(t_array, sigma_x_analytical, 'm--', linewidth=1.5, alpha=0.7, label='Analytical')
ax2.set_xlabel('Time (ℏ/E₀)', fontsize=12)
ax2.set_ylabel('σₓ(t)', fontsize=12)
ax2.set_title('Standard Deviation of Position vs Time', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
ax2.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('quantum_two_level_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Plot saved to quantum_two_level_analysis.png")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
Key Results:
- α = {alpha}
- c₀ = {c0:.4f}, c₁ = {c1:.4f}
- ⟨X⟩(t) oscillates with frequency ω = {omega:.4f}
- σₓ(t) also oscillates, indicating quantum uncertainty varies with time
- The system exhibits coherent oscillations between position states
""")

print("\nDone! ✓")