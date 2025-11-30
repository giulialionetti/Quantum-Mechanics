import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from scipy.special import hermite
from scipy.special import factorial

class QuantumHarmonicOscillator:
    """
    Quantum Harmonic Oscillator with ladder operator visualizations.
    """
    
    def __init__(self, m=1.0, omega=1.0, hbar=1.0):
        """
        Initialize the quantum harmonic oscillator.
        
        Parameters:
        m: mass
        omega: angular frequency
        hbar: reduced Planck constant (set to 1 for natural units)
        """
        self.m = m
        self.omega = omega
        self.hbar = hbar
        self.x0 = np.sqrt(hbar / (m * omega))  # characteristic length scale
        
    def psi_n(self, x, n):
        """
        Calculate the wavefunction for the nth energy eigenstate.
        
        Parameters:
        x: position array
        n: quantum number (0, 1, 2, ...)
        
        Returns:
        wavefunction psi_n(x)
        """
        # Normalization constant
        N_n = 1.0 / np.sqrt(2**n * factorial(n)) * (self.m * self.omega / (np.pi * self.hbar))**(1/4)
        
        # Dimensionless position
        xi = x / self.x0
        
        # Hermite polynomial
        H_n = hermite(n)
        
        # Wavefunction
        psi = N_n * np.exp(-xi**2 / 2) * H_n(xi)
        
        return psi
    
    def apply_creation(self, coeffs):
        """
        Apply creation operator to a state represented by coefficients.
        
        â†|n⟩ = sqrt(n+1)|n+1⟩
        
        Parameters:
        coeffs: array of coefficients for |0⟩, |1⟩, |2⟩, ...
        
        Returns:
        new coefficients after applying â†
        """
        new_coeffs = np.zeros(len(coeffs))
        for n in range(len(coeffs) - 1):
            new_coeffs[n + 1] = np.sqrt(n + 1) * coeffs[n]
        return new_coeffs
    
    def apply_annihilation(self, coeffs):
        """
        Apply annihilation operator to a state.
        
        â|n⟩ = sqrt(n)|n-1⟩
        
        Parameters:
        coeffs: array of coefficients for |0⟩, |1⟩, |2⟩, ...
        
        Returns:
        new coefficients after applying â
        """
        new_coeffs = np.zeros(len(coeffs))
        for n in range(1, len(coeffs)):
            new_coeffs[n - 1] = np.sqrt(n) * coeffs[n]
        return new_coeffs
    
    def state_to_wavefunction(self, x, coeffs):
        """
        Convert state coefficients to position-space wavefunction.
        
        Parameters:
        x: position array
        coeffs: array of coefficients for |0⟩, |1⟩, |2⟩, ...
        
        Returns:
        psi(x) = sum_n c_n * psi_n(x)
        """
        psi = np.zeros_like(x)
        for n, c_n in enumerate(coeffs):
            if abs(c_n) > 1e-10:  # Skip negligible contributions
                psi += c_n * self.psi_n(x, n)
        return psi


def create_interactive_visualization():
    """
    Create an interactive visualization of ladder operators.
    """
    qho = QuantumHarmonicOscillator()
    
    # Position space
    x = np.linspace(-5, 5, 500)
    
    # Initial state: |2⟩ (3rd energy level)
    n_max = 10
    initial_n = 2
    coeffs = np.zeros(n_max)
    coeffs[initial_n] = 1.0
    
    # Create figure
    fig = plt.figure(figsize=(14, 10))
    
    # Wavefunction plot
    ax_wave = plt.subplot(2, 2, (1, 2))
    psi_initial = qho.state_to_wavefunction(x, coeffs)
    line_initial, = ax_wave.plot(x, np.real(psi_initial), 'b-', linewidth=2, label='Initial State')
    line_final, = ax_wave.plot(x, np.zeros_like(x), 'r--', linewidth=2, label='After Operator')
    ax_wave.set_xlabel('Position x', fontsize=12)
    ax_wave.set_ylabel('ψ(x)', fontsize=12)
    ax_wave.set_title('Wavefunction in Position Space', fontsize=14, fontweight='bold')
    ax_wave.grid(True, alpha=0.3)
    ax_wave.legend(fontsize=10)
    ax_wave.set_ylim(-1, 1)
    
    # Probability density plot
    ax_prob = plt.subplot(2, 2, 3)
    prob_initial = np.abs(psi_initial)**2
    fill_initial = ax_prob.fill_between(x, prob_initial, alpha=0.5, color='blue', label='Initial |ψ|²')
    line_prob_final, = ax_prob.plot(x, np.zeros_like(x), 'r-', linewidth=2, label='Final |ψ|²')
    ax_prob.set_xlabel('Position x', fontsize=12)
    ax_prob.set_ylabel('|ψ(x)|²', fontsize=12)
    ax_prob.set_title('Probability Density', fontsize=14, fontweight='bold')
    ax_prob.grid(True, alpha=0.3)
    ax_prob.legend(fontsize=10)
    
    # Energy level diagram
    ax_energy = plt.subplot(2, 2, 4)
    energy_levels = np.arange(n_max) + 0.5
    bars_initial = ax_energy.barh(energy_levels, np.abs(coeffs)**2, height=0.8, 
                                   alpha=0.6, color='blue', label='Initial')
    bars_final = ax_energy.barh(energy_levels, np.zeros(n_max), height=0.4, 
                                 alpha=0.6, color='red', label='Final')
    ax_energy.set_xlabel('Population |cₙ|²', fontsize=12)
    ax_energy.set_ylabel('Energy Level n', fontsize=12)
    ax_energy.set_title('Energy Eigenstate Populations', fontsize=14, fontweight='bold')
    ax_energy.set_ylim(-0.5, n_max - 0.5)
    ax_energy.grid(True, alpha=0.3, axis='x')
    ax_energy.legend(fontsize=10)
    
    # Store current state
    state = {'coeffs': coeffs.copy()}
    
    def update_plots():
        """Update all plots with current state."""
        # Update wavefunction
        psi_current = qho.state_to_wavefunction(x, state['coeffs'])
        line_final.set_ydata(np.real(psi_current))
        
        # Update probability density
        prob_current = np.abs(psi_current)**2
        line_prob_final.set_ydata(prob_current)
        
        # Update energy levels
        populations = np.abs(state['coeffs'])**2
        for bar, pop in zip(bars_final, populations):
            bar.set_width(pop)
        
        # Adjust y-limits for wavefunction
        all_vals = np.concatenate([np.real(psi_initial), np.real(psi_current)])
        y_margin = 0.1 * (np.max(all_vals) - np.min(all_vals))
        ax_wave.set_ylim(np.min(all_vals) - y_margin, np.max(all_vals) + y_margin)
        
        # Adjust y-limits for probability
        max_prob = max(np.max(prob_initial), np.max(prob_current))
        ax_prob.set_ylim(0, max_prob * 1.1)
        
        fig.canvas.draw_idle()
    
    # Button callbacks
    def apply_creation_op(event):
        state['coeffs'] = qho.apply_creation(state['coeffs'])
        # Renormalize
        norm = np.sqrt(np.sum(np.abs(state['coeffs'])**2))
        if norm > 1e-10:
            state['coeffs'] /= norm
        update_plots()
    
    def apply_annihilation_op(event):
        state['coeffs'] = qho.apply_annihilation(state['coeffs'])
        # Renormalize
        norm = np.sqrt(np.sum(np.abs(state['coeffs'])**2))
        if norm > 1e-10:
            state['coeffs'] /= norm
        update_plots()
    
    def reset_state(event):
        state['coeffs'] = np.zeros(n_max)
        state['coeffs'][initial_n] = 1.0
        update_plots()
    
    # Add buttons
    ax_btn_creation = plt.axes([0.25, 0.02, 0.15, 0.04])
    btn_creation = Button(ax_btn_creation, 'Apply â† (Creation)', color='lightgreen', hovercolor='green')
    btn_creation.on_clicked(apply_creation_op)
    
    ax_btn_annihilation = plt.axes([0.45, 0.02, 0.15, 0.04])
    btn_annihilation = Button(ax_btn_annihilation, 'Apply â (Annihilation)', color='lightcoral', hovercolor='red')
    btn_annihilation.on_clicked(apply_annihilation_op)
    
    ax_btn_reset = plt.axes([0.65, 0.02, 0.1, 0.04])
    btn_reset = Button(ax_btn_reset, 'Reset', color='lightgray', hovercolor='gray')
    btn_reset.on_clicked(reset_state)
    
    plt.suptitle('Quantum Ladder Operators Visualization', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.show()


if __name__ == "__main__":
    print("Quantum Ladder Operators Visualizer")
    print("=" * 50)
    print("This tool visualizes the action of creation (â†) and")
    print("annihilation (â) operators on quantum harmonic oscillator states.")
    print("\nClick the buttons to apply operators and see how the")
    print("wavefunction and energy level populations change!")
    print("=" * 50)
    
    create_interactive_visualization()