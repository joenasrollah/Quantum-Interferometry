"""
Talbot Carpet Forward Simulation
================================
Angular-spectrum non-paraxial propagation of a binary transmission grating.

Setup matching experimental parameters:
  - 5 lines-per-mm grating -> period d = 0.2 mm
  - 2 mm wide illuminating beam
  - Wavelength: 632.8 nm (HeNe laser)
  - z-axis: 0 -> 1.25 * Z_T
  - y-axis: position along sensor / grating
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def run_simulation(lpm=5.0, lam_nm=632.8, beam_width_mm=2.0, z_factor=1.25, save_fig=True):
    # Physical parameters
    d = 1.0 / lpm                    # grating period in mm (0.2 mm)[cite: 5, 8]
    lam = lam_nm * 1e-6              # wavelength in mm (632.8 nm)
    Z_T = 2 * (d**2) / lam           # Talbot length in mm[cite: 5, 6]

    print(f"Grating period d   = {d:.4f} mm")
    print(f"Theoretical Z_T    = {Z_T:.3f} mm ({Z_T / 10:.2f} cm)")

    # Simulation grid
    y_half = 1.8                     # sensor span +/- 1.8 mm
    n_y = 800
    y = np.linspace(-y_half, y_half, n_y)

    z_max = z_factor * Z_T
    n_z = 1000
    z = np.linspace(1e-6 * Z_T, z_max, n_z)  # avoid z=0 phase singularity

    # Angular-spectrum propagation
    k = 2 * np.pi / lam
    N = 40                           # propagating spatial modes
    modes = np.arange(-N, N + 1)

    # Gaussian beam envelope across aperture
    sigma = beam_width_mm / (2 * np.sqrt(2 * np.log(2)))
    envelope = np.exp(-y**2 / (2 * sigma**2))

    E = np.zeros((n_y, n_z), dtype=complex)

    for n in modes:
        if n == 0:
            cn = 0.5
        else:
            cn = np.sin(n * np.pi * 0.5) / (n * np.pi)

        kxn = 2 * np.pi * n / d
        kz_sq = k**2 - kxn**2
        if kz_sq <= 0:
            continue                 # skip evanescent modes

        kzn = np.sqrt(kz_sq)
        phase_y = np.exp(1j * kxn * y)
        phase_z = np.exp(1j * kzn * z)

        E += cn * np.outer(phase_y * envelope, phase_z)

    I = np.abs(E)**2
    I /= I.max()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
    im = ax.imshow(
        I,
        aspect='auto',
        origin='lower',
        extent=[0, z_max, y[0], y[-1]],
        cmap='hot',
        vmin=0, vmax=1,
        interpolation='bilinear'
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label('Normalised Intensity', fontsize=10)

    # Fractional Talbot planes
    frac_planes = [0.25, 0.5, 0.75, 1.0, 1.25]
    frac_labels = [r'$Z_T/4$', r'$Z_T/2$', r'$3Z_T/4$', r'$Z_T$', r'$5Z_T/4$']
    for fz, lbl in zip(frac_planes, frac_labels):
        zval = fz * Z_T
        ax.axvline(zval, color='cyan', lw=0.8, ls='--', alpha=0.75)
        ax.text(zval + 0.003 * z_max, y[-1] * 0.90, lbl,
                color='cyan', fontsize=8, ha='left', va='top', fontfamily='monospace')

    ax.set_xlabel(r'Propagation Distance $z$ / $Z_T$', fontsize=11)
    ax.set_ylabel('Position Along Sensor (mm)', fontsize=11)
    ax.set_title(
        rf'Talbot Carpet Simulation (5 lp/mm, $\lambda = {lam_nm}\,\mathrm{{nm}}$, $Z_T = {Z_T:.1f}\,\mathrm{{mm}}$)',
        fontsize=11
    )

    ax.xaxis.set_major_locator(ticker.MultipleLocator(Z_T * 0.25))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f'{v / Z_T:.2f}'))

    plt.tight_layout()
    if save_fig:
        plt.savefig('assets/simulated_carpet.png', dpi=150, bbox_inches='tight')
        print("Figure saved to assets/simulated_carpet.png")
    return fig, ax, I


if __name__ == "__main__":
    run_simulation()
    plt.show()