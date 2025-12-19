

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

# Set up the box
L = 1.0
x = np.linspace(0, L, 1000)

# Define the two wavefunctions
psi_1 = np.sqrt(2) * np.sin(1 * np.pi * x / L)  # n=1
psi_2 = np.sqrt(2) * np.sin(2 * np.pi * x / L)  # n=2

# Create output directory
output_dir = './qm_animation_frames'
os.makedirs(output_dir, exist_ok=True)

n_frames = 30
alphas = np.linspace(0, 1, n_frames)

for i, alpha in enumerate(alphas):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Quantum Interference: Building the Superposition (Frame {i+1}/{n_frames})', 
                 fontsize=16, fontweight='bold')
    
    ax1, ax2, ax3, ax4 = axes.flatten()
    
   
    if alpha < 0.01:
        psi_super = psi_1.copy()
        label_text = "|n=1⟩ only"
        progress = 0
    else:
        weight_1 = 1.0 / np.sqrt(1 + alpha**2)
        weight_2 = alpha / np.sqrt(1 + alpha**2)
        psi_super = weight_1 * psi_1 + weight_2 * psi_2
        progress = int(alpha * 100)
        if alpha < 0.99:
            label_text = f"Adding |n=2⟩... {progress}%"
        else:
            label_text = "(|n=1⟩ + |n=2⟩)/√2 "
    
    
    ax1.plot(x, psi_1, 'b-', linewidth=2.5, label='ψ₁ (n=1)', alpha=0.8)
    ax1.plot(x, psi_2 * alpha, 'r-', linewidth=2.5, label=f'ψ₂ (n=2) × {alpha:.2f}', alpha=0.8)
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax1.fill_between(x, 0, psi_1, alpha=0.2, color='blue')
    ax1.fill_between(x, 0, psi_2 * alpha, where=(psi_2>0), alpha=0.2, color='red', interpolate=True)
    ax1.fill_between(x, 0, psi_2 * alpha, where=(psi_2<0), alpha=0.2, color='orange', interpolate=True)
    ax1.set_ylabel('Wavefunction', fontsize=12)
    ax1.set_title('Individual States', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([0, 1])
    ax1.set_ylim([-2, 2])
    
   
    ax2.plot(x, psi_1, 'b--', linewidth=1, alpha=0.3, label='ψ₁')
    ax2.plot(x, psi_2 * alpha, 'r--', linewidth=1, alpha=0.3, label='ψ₂')
    ax2.plot(x, psi_super, 'purple', linewidth=3.5, label=label_text)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.fill_between(x, 0, psi_super, alpha=0.4, color='purple')
    ax2.set_ylabel('Wavefunction', fontsize=12)
    ax2.set_title('Superposition ψ₁ + ψ₂', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([-2.5, 2.5])
    
    
    if alpha > 0.8:
        ax2.annotate('Constructive\nInterference', xy=(0.25, 1.7), fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9),
                    ha='center')
        ax2.annotate('Destructive\nInterference', xy=(0.75, -0.3), fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.9),
                    ha='center')
    
    
    prob_super = psi_super**2
    ax3.plot(x, prob_super, 'purple', linewidth=3.5)
    ax3.fill_between(x, 0, prob_super, alpha=0.5, color='purple')
    ax3.set_ylabel('Probability |ψ(x)|²', fontsize=12)
    ax3.set_xlabel('Position x', fontsize=12)
    ax3.set_title('Where Will We Find The Particle?', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim([0, 1])
    ax3.set_ylim([0, 3.5])
    
    # Mark peaks
    if alpha > 0.8:
        left_peak_idx = np.argmax(prob_super[:500])
        right_peak_idx = 500 + np.argmax(prob_super[500:])
        ax3.plot(x[left_peak_idx], prob_super[left_peak_idx], 'go', 
                markersize=15, label=f'Left: {prob_super[left_peak_idx]:.2f}', zorder=5)
        ax3.plot(x[right_peak_idx], prob_super[right_peak_idx], 'ro', 
                markersize=15, label=f'Right: {prob_super[right_peak_idx]:.2f}', zorder=5)
        ax3.legend(loc='upper right', fontsize=11)
    
   
    idx_025 = 250
    idx_075 = 750
    
    values_at_025 = [psi_1[idx_025], psi_2[idx_025] * alpha, psi_super[idx_025]]
    values_at_075 = [psi_1[idx_075], psi_2[idx_075] * alpha, psi_super[idx_075]]
    
    x_pos = np.arange(3)
    width = 0.35
    
    ax4.bar(x_pos - width/2, values_at_025, width, 
            label='At x=0.25 (left)', color=['blue', 'red', 'purple'], alpha=0.7)
    ax4.bar(x_pos + width/2, values_at_075, width, 
            label='At x=0.75 (right)', color=['blue', 'red', 'purple'], alpha=0.4)
    
    ax4.axhline(y=0, color='k', linestyle='-', linewidth=1)
    ax4.set_ylabel('Wavefunction Value', fontsize=12)
    ax4.set_xlabel('Component', fontsize=12)
    ax4.set_title('Comparing Left vs Right', fontsize=13, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(['ψ₁', 'ψ₂', 'Sum'])
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.set_ylim([-1.6, 2])
    
    if alpha > 0.8:
        ax4.text(2, 1.5, 'LEFT:\nBoth +\n→ ADD', ha='center', fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        ax4.text(2, -1.2, 'RIGHT:\nOpposite\n→ CANCEL', ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save frame
    filename = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    
    if (i+1) % 5 == 0:
        print(f"  ✓ Frame {i+1}/{n_frames} complete ({progress}%)")

print(f"\n✓ All {n_frames} frames created!")


frame_files = sorted(glob.glob(os.path.join(output_dir, 'frame_*.png')))
print(f"Found {len(frame_files)} frames")


images = []
for f in frame_files:
    img = Image.open(f)
    images.append(img)

output_gif = './quantum_interference.gif'
images[0].save(
    output_gif,
    save_all=True,
    append_images=images[1:],
    duration=100,  
    loop=0  
)

file_size_mb = os.path.getsize(output_gif) / 1024 / 1024
print(f"\n✓ Animation saved as {output_gif} ({file_size_mb:.2f} MB)")