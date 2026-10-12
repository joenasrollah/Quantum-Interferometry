"""
Appendix B: Heisenberg Uncertainty with Error Propagation
Extends Appendix A to compute transverse momentum uncertainty from measured
angular widths and plots Delta p against 1 / Delta x with propagated error bounds.
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

slitRange = np.arange(2, 9, 1)
x = np.arange(0, 1280, 1)
colAvg = 8
meterPerPixel = 5.2e-6  # size of pixel in metres
L = 0.9                 # length from grating to camera in metres
h = 6.63e-34            # Planck constant (J s)
wavelength = 633e-9     # HeNe laser wavelength in metres

angleList = []
diffList = []

for slit in slitRange:
    filename = f"{slit / 10:.1f}mm.png"
    im = Image.open(filename).convert('L')
    na = np.array(im)

    row_center = na.shape[0] // 2
    midRowsAvg = np.average(
        na[(row_center - colAvg // 2):(row_center + colAvg // 2), :],
        axis=0
    )

    rowsSmooth = gaussian_filter1d(midRowsAvg, sigma=3)
    peaks, _ = find_peaks(rowsSmooth, width=10, distance=150, height=4)

    if len(peaks) > 2:
        centralMaxima = np.argmax(rowsSmooth[peaks])
        difference = peaks[centralMaxima + 1] - peaks[centralMaxima - 1]
    elif len(peaks) == 2:
        difference = (peaks[1] - peaks[0]) * 2
    else:
        difference = 0

    angularWidth = (meterPerPixel * difference) / L
    angleList.append(angularWidth)
    diffList.append(difference)

# Momentum uncertainty calculations
deltaP = np.array(angleList) * (h / wavelength)
deltaXreciprocal = 1.0 / (slitRange * 1e-4)

# Error propagation
sigmaL = 0.001     # uncertainty in camera distance (m)
sigmaDiff = 50.0   # uncertainty in peak separation (pixels)
diffArray = np.array(diffList, dtype=float)

sigmaP = deltaP * np.sqrt((sigmaDiff / diffArray) ** 2 + (sigmaL / L) ** 2)

# Linear fit and plotting
plt.figure()
plt.errorbar(deltaXreciprocal, deltaP, yerr=sigmaP, fmt='bo', capsize=4, label="Measured Uncertainty")

# Linear fit
slope, intercept = np.polyfit(deltaXreciprocal, deltaP, 1)
fit_x = np.linspace(min(deltaXreciprocal), max(deltaXreciprocal), 100)
plt.plot(fit_x, slope * fit_x + intercept, 'r-', label=f"Fit: Slope = {slope:.2e}")

plt.xlabel(r"$1 / \Delta x$ ($m^{-1}$)")
plt.ylabel(r"$\Delta p$ ($kg\,m\,s^{-1}$)")
plt.title("Heisenberg Uncertainty: Transverse Momentum vs Position Constraint")
plt.legend()
plt.savefig("heisenberg_uncertainty_fit.png")
plt.show()

print(f"Momentum-Position Uncertainty Gradient: {slope:.3e} kg m^2 s^-1")