"""
Change of Basis in Quantum Mechanics
From Energy Eigenstates to Position Eigenstates

This code demonstrates how to go from an energy representation to a position representation (and vice versa)
for a particle in a box (1D).
The particle is confined in a 1D box of length L with infinite potential walls at x=0 and x=L.

"""

import numpy as np
import matplotlib.pyplot as plt
import os

class ParticleInBox:
    
    def __init__(self, L=1.0, n_max=10, n_points=1000):
        
        self.L = L
        self.n_max = n_max
        self.x = np.linspace(0, L, n_points)
        self.dx = self.x[1] - self.x[0]
        
    def position_wavefunction(self, n, x):
        
        n_quantum = n + 1
        
        normalization = np.sqrt(2.0 / self.L)
        psi = normalization * np.sin(n_quantum * np.pi * x / self.L)
        
        return psi
    
    def energy_to_position(self, coefficients):
       
        coefficients = np.array(coefficients)
        n_states = len(coefficients)
        
        psi_x = np.zeros_like(self.x, dtype=complex)
        
        for n in range(n_states):
            psi_x += coefficients[n] * self.position_wavefunction(n, self.x)
        
        return psi_x
    
    def position_to_energy(self, psi_x):
       
        coefficients = np.zeros(self.n_max, dtype=complex)
        
        for n in range(self.n_max):
            psi_n = self.position_wavefunction(n, self.x)
            # Inner product: c_n = ⟨n|ψ⟩ = ∫ ψ_n*(x) ψ(x) dx
            # Use trapezoidal rule for numerical integration
            coefficients[n] = np.trapz(psi_n * psi_x, self.x)
        
        return coefficients


def example_ground_state(output_dir='./'):
   
    print("=" * 60)
    print("Example 1: Ground State |n=1⟩")
    print("=" * 60)
    
    pib = ParticleInBox(L=1.0, n_max=5)
    
    # Ground state in energy basis (first state, n=1)
    c_n = np.array([1.0, 0, 0, 0, 0])
    print(f"Energy basis coefficients: {c_n}")
    print(f"This represents the state: |n=1⟩")
    
    # Transform to position basis
    psi_x = pib.energy_to_position(c_n)
    
    # Transform back to energy basis (verification)
    c_n_recovered = pib.position_to_energy(psi_x)
    print(f"Recovered coefficients: {np.abs(c_n_recovered)}")
    print(f"Error: {np.max(np.abs(c_n - c_n_recovered)):.2e}")
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.stem(range(1, len(c_n)+1), np.abs(c_n)**2, basefmt=' ')
    ax1.set_xlabel('Quantum number n')
    ax1.set_ylabel('|c_n|²')
    ax1.set_title('Energy Basis (Probability)')
    ax1.set_xticks(range(1, len(c_n)+1))
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(pib.x, np.abs(psi_x)**2, 'b-', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Position x (box length)')
    ax2.set_ylabel('|ψ(x)|²')
    ax2.set_title('Position Basis (Probability Density)')
    ax2.set_xlim([0, 1])
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = os.path.join(output_dir, 'ground_state_simple.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {filename}\n")
    plt.close()


def example_superposition(output_dir='./'):
    """Example: Equal superposition of n=1 and n=2"""
    print("=" * 60)
    print("Example 2: Superposition (|n=1⟩ + |n=2⟩)/√2")
    print("=" * 60)
    
    pib = ParticleInBox(L=1.0, n_max=5)
    
    # Superposition of first two states
    c_n = np.array([1.0, 1.0, 0, 0, 0]) / np.sqrt(2)
    print(f"Energy basis coefficients: {c_n}")
    
    # Transform to position basis
    psi_x = pib.energy_to_position(c_n)
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.stem(range(1, len(c_n)+1), np.abs(c_n)**2, basefmt=' ')
    ax1.set_xlabel('Quantum number n')
    ax1.set_ylabel('|c_n|²')
    ax1.set_title('Energy Basis (Probability)')
    ax1.set_xticks(range(1, len(c_n)+1))
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(pib.x, np.abs(psi_x)**2, 'r-', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Position x (box length)')
    ax2.set_ylabel('|ψ(x)|²')
    ax2.set_title('Position Basis (Probability Density)')
    ax2.set_xlim([0, 1])
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = os.path.join(output_dir, 'superposition_simple.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {filename}\n")
    plt.close()


def example_localized_packet(output_dir='./'):
    """Example: Localized wavepacket decomposed into energy eigenstates"""
    print("=" * 60)
    print("Example 3: Localized Gaussian Packet")
    print("=" * 60)
    
    pib = ParticleInBox(L=1.0, n_max=30)
    
    # Create a Gaussian wavepacket centered at x=0.3
    x0 = 0.3
    sigma = 0.1
    psi_x_gaussian = np.exp(-(pib.x - x0)**2 / (2 * sigma**2))
    
    # Set to zero outside the box (enforce boundary conditions)
    psi_x_gaussian[pib.x <= 0] = 0
    psi_x_gaussian[pib.x >= pib.L] = 0
    
    # Normalize
    norm = np.sqrt(np.trapz(np.abs(psi_x_gaussian)**2, pib.x))
    psi_x_gaussian /= norm
    
    # Transform to energy basis
    c_n = pib.position_to_energy(psi_x_gaussian)
    
    print(f"First 5 energy coefficients: {c_n[:5]}")
    print(f"Sum of probabilities: {np.sum(np.abs(c_n)**2):.4f}")
    print(f"Number of significant components: {np.sum(np.abs(c_n)**2 > 0.01)}")
    
    # Reconstruct
    psi_x_reconstructed = pib.energy_to_position(c_n)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Energy basis - all states
    axes[0, 0].stem(range(1, len(c_n)+1), np.abs(c_n)**2, basefmt=' ')
    axes[0, 0].set_xlabel('Quantum number n')
    axes[0, 0].set_ylabel('|c_n|²')
    axes[0, 0].set_title('Energy Basis - All States')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Energy basis - first 10 states
    axes[0, 1].bar(range(1, 11), np.abs(c_n[:10])**2, alpha=0.7)
    axes[0, 1].set_xlabel('Quantum number n')
    axes[0, 1].set_ylabel('|c_n|²')
    axes[0, 1].set_title('Energy Basis - First 10 States')
    axes[0, 1].set_xticks(range(1, 11))
    axes[0, 1].grid(True, alpha=0.3)
    
    # Position basis - comparison
    axes[1, 0].plot(pib.x, np.abs(psi_x_gaussian)**2, 'g-', linewidth=2, label='Original')
    axes[1, 0].plot(pib.x, np.abs(psi_x_reconstructed)**2, 'r--', linewidth=2, label='Reconstructed')
    axes[1, 0].set_xlabel('Position x (box length)')
    axes[1, 0].set_ylabel('|ψ(x)|²')
    axes[1, 0].set_title('Position Basis (Probability Density)')
    axes[1, 0].legend()
    axes[1, 0].set_xlim([0, 1])
    axes[1, 0].grid(True, alpha=0.3)
    
    # Wavefunction (real part)
    axes[1, 1].plot(pib.x, np.real(psi_x_gaussian), 'b-', linewidth=2, label='Original')
    axes[1, 1].plot(pib.x, np.real(psi_x_reconstructed), 'r--', linewidth=1.5, label='Reconstructed')
    axes[1, 1].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    axes[1, 1].set_xlabel('Position x (box length)')
    axes[1, 1].set_ylabel('Re[ψ(x)]')
    axes[1, 1].set_title('Wavefunction (Real Part)')
    axes[1, 1].legend()
    axes[1, 1].set_xlim([0, 1])
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = os.path.join(output_dir, 'localized_packet_simple.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {filename}\n")
    plt.close()


def show_individual_states(output_dir='./'):
    """Show what the first few energy eigenstates look like"""
    print("=" * 60)
    print("Example 4: Individual Energy Eigenstates")
    print("=" * 60)
    
    pib = ParticleInBox(L=1.0, n_max=5)
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    
    for n in range(6):
        # Create state with only this quantum number
        c_n = np.zeros(5)
        if n < 5:
            c_n[n] = 1.0
            psi_x = pib.energy_to_position(c_n)
            
            axes[n].plot(pib.x, psi_x, 'b-', linewidth=2, label='ψ(x)')
            axes[n].plot(pib.x, np.abs(psi_x)**2, 'r-', linewidth=2, label='|ψ(x)|²')
            axes[n].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            axes[n].set_xlabel('Position x')
            axes[n].set_ylabel('Wavefunction')
            axes[n].set_title(f'State |n={n+1}⟩')
            axes[n].set_xlim([0, 1])
            axes[n].grid(True, alpha=0.3)
            axes[n].legend()
            
            print(f"State n={n+1}: {n+1} nodes (zeros) inside the box")
    
    # Remove extra subplot
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    filename = os.path.join(output_dir, 'individual_states_simple.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {filename}\n")
    plt.close()


def demonstrate_orthonormality(output_dir='./'):
    """Verify orthonormality: ⟨m|n⟩ = δ_mn"""
    print("=" * 60)
    print("Example 5: Orthonormality Check")
    print("=" * 60)
    
    pib = ParticleInBox(L=1.0, n_max=5)
    
    # Compute overlap matrix
    overlap = np.zeros((5, 5))
    
    for m in range(5):
        psi_m = pib.position_wavefunction(m, pib.x)
        for n in range(5):
            psi_n = pib.position_wavefunction(n, pib.x)
            overlap[m, n] = np.trapz(psi_m * psi_n, pib.x)
    
    print("Overlap matrix ⟨m|n⟩:")
    print(np.round(overlap, 4))
    print("\nShould be identity matrix (δ_mn)")
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(np.abs(overlap), cmap='RdBu', vmin=-0.1, vmax=1.1)
    ax.set_xlabel('n')
    ax.set_ylabel('m')
    ax.set_title('Overlap Matrix |⟨m|n⟩|')
    
    # Adjust ticks to show quantum numbers (1-5 instead of 0-4)
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(range(1, 6))
    ax.set_yticklabels(range(1, 6))
    
    # Add text annotations
    for i in range(5):
        for j in range(5):
            text = ax.text(j, i, f'{overlap[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=10)
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    filename = os.path.join(output_dir, 'orthonormality_simple.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {filename}\n")
    plt.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Quantum Mechanics: Change of Basis")
    print("Particle in a Box")
    print("Wavefunctions: ψ_n(x) = √(2/L) sin(nπx/L)")
    print("="*60 + "\n")
    
    # Create output directory
    output_dir = './qm_plots_simple'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving plots to: {os.path.abspath(output_dir)}\n")
    
    show_individual_states(output_dir)
    example_ground_state(output_dir)
    example_superposition(output_dir)
    example_localized_packet(output_dir)
    demonstrate_orthonormality(output_dir)
    
    print("="*60)
    print("All examples completed!")
    print(f"All plots saved in: {os.path.abspath(output_dir)}")
    print("="*60)
