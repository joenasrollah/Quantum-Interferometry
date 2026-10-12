# Quantum Interferometry in the Optical Near and Far Field

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Experimental laser metrology and numerical simulation of near-field Talbot self-imaging and far-field diffraction using a 633 nm HeNe bench.

Authored by Joseph Nasrollahzadeh, School of Physics & Astronomy, University of Nottingham.

---
## Abstract

This report investigates the wave nature of light across both the Fraunhofer (far-field) and Fresnel (near-field) diffraction regimes. Using a 633 nm Helium-Neon (HeNe) laser, far-field single-slit diffraction was used to test the Heisenberg Uncertainty Principle.

Analysis yielded a momentum-position uncertainty gradient of $(1.82 \pm 0.17) \times 10^{-33}\text{ kg m}^2\text{s}^{-1}$, equating to approximately $32\,\hbar/2$. This expected inflation arises from defining uncertainty strictly by the physical slit width and primary diffraction nulls, which overestimates the spatial bound when compared to the Gaussian standard-deviation convention. In the near-field regime, the spatial evolution of the interference pattern from a 5 lines/mm diffraction grating was swept via longitudinal translation of a CCD camera to construct a high-resolution 'Talbot carpet'. Fractional self-imaging was successfully observed at $\frac{1}{4}$, $\frac{1}{2}$, and $\frac{3}{4}$ of the Talbot distance. By accounting for a mechanical offset at the sensor plane, the fundamental Talbot distance was measured as $Z_T = 12.6\text{ cm}$, showing precise agreement with theoretical predictions.

---
## Key Experimental & Engineering Highlights

* **Optomechanical Alignment & Beam Expansion:** Designed a custom Keplerian telescope using 50 mm plano-convex and 125 mm convex lenses (175 mm separation) to expand the 633 nm beam. This prevented boundary-aperture clipping and established uniform phase illumination across the 5 lines/mm diffraction grating.
* **Systematic Hardware Offset Diagnosis:** Isolated an internal 1.82 cm mechanical recess offset within the CCD sensor housing that initially skewed measured Talbot distances by 14%. Applying this hardware correction yielded an empirical primary self-imaging distance of $Z_T = 12.60\text{ cm}$, matching theoretical predictions ($12.64\text{ cm}$) to within **0.4%**.
* **Automated Data Processing Pipeline:** Built Python data pipelines (NumPy, SciPy) utilising 1D Gaussian smoothing filters ($\sigma = 3$) and automated peak-detection algorithms to extract intensity nulls and construct 2D Talbot carpets from longitudinal translation sweeps.
* **Heisenberg Uncertainty Boundary Verification:** Quantified transverse momentum-position uncertainty gradients across variable aperture widths ($0.2\text{ mm}$ to $0.8\text{ mm}$), yielding a linear slope of $(1.82 \pm 0.17) \times 10^{-33}\text{ kg m}^2\text{s}^{-1}$ with propagated error bounds.

---

## Theory vs Empirical Reconstruction

| Forward Numerical Simulation (Angular Spectrum) | Empirical Reconstruction (Longitudinal CCD Sweep) |
| :---: | :---: |
| ![Simulated Carpet](assets/simulated_carpet.png) | ![Reconstructed Carpet](assets/reconstructed_carpet.png) |
| *Exact non-paraxial angular-spectrum propagation* | *Automated centroid tracking & row stacking* |

---

## Repository Structure

```text
Quantum-Interferometry/
├── notebooks/
│   └── interactive_talbot.ipynb       # Interactive parameter sliders (wavelength, grating period)
├── paper/
│   └── Quantum_Interferometry_in_the_Optical_Near_and_Far_Field.pdf  # Authored 24-page report
├── src/
│   ├── A_single_slit_diffraction.py   # Appendix A: Fraunhofer single-slit peak extraction
│   ├── B_heisenberg_uncertainty.py    # Appendix B: Momentum uncertainty & error propagation
│   ├── C_grating_sinc_fit.py          # Appendix C: Multi-slit interference & sinc² envelope
│   ├── D_talbot_carpet.py             # Appendix D: Near-field 2D carpet reconstruction
│   └── simulate_carpet.py             # Forward wave simulation (angular-spectrum method)
├── assets/
│   ├── simulated_carpet.png           # Simulation output figure
│   └── reconstructed_carpet.png       # Experimental carpet output figure
├── demo.py                            # Standalone demonstration & verification runner
├── requirements.txt                   # Dependency environment specification
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quickstart

### 1. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/joenasrollah/optical-interferometry-metrology.git](https://github.com/joenasrollah/optical-interferometry-metrology.git)
cd optical-interferometry-metrology
pip install -r requirements.txt
```

### 2. Run the Verification Demo
Run the root demonstration script to simulate the Talbot carpet and verify the 1.82 cm sensor casing calibration:

```bash
python demo.py
```

### 3. Interactive Notebook
To explore the non-paraxial propagation model interactively:

```bash
jupyter notebook notebooks/interactive_talbot.ipynb
```
