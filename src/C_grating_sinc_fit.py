"""
Appendix C: Sinc Function Fitting to Multi-Slit Diffraction Pattern
Loads a filtered diffraction image, overlays a theoretical sinc^2 envelope
onto the measured intensity profile, and identifies diffraction order peaks.
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

slitRange = [20]
x = np.arange(0, 1280, 1)
colAvg = 8
meterPerPixel = 5.2e-6  # size of pixel in metres
L = 0.9                 # length from grating to camera in metres
h = 6.63e-34
wavelength = 633e-9     # HeNe laser wavelength in metres

def sinc(width):
    # Centered at pixel 642 matching the central optical axis
    return np.sinc((x - 642) / width)

for slit in slitRange:
    im = Image.open(f"{slit / 10:.1f} filter.png").convert('L')
    na = np.array(im)

    row_center = na.shape[0] // 2
    midRowsAvg = np.average(
        na[(row_center - colAvg // 2):(row_center + colAvg // 2), :],
        axis=0
    )

    rowsSmooth = gaussian_filter1d(midRowsAvg, sigma=3)

    plt.figure()
    plt.plot(x, midRowsAvg, label="Diffraction Grating (5 lines/mm)")
    plt.plot(x, (12.25 * sinc(245)) ** 2, label=r"Single-Slit $\mathrm{sinc}^2$ Envelope")

    peaks, _ = find_peaks(rowsSmooth, width=10, distance=100, height=4)
    plt.plot(peaks, np.zeros(len(peaks)), "or", label="Detected Maxima")

    plt.xlabel("Pixel Position")
    plt.ylabel("Pixel Intensity")
    plt.title("Grating Interference Modulated by Single-Slit Envelope")
    plt.legend()
    plt.savefig("grating_sinc_envelope.png")
    plt.show()