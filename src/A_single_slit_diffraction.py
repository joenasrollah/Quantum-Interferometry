"""
Appendix A: Single-Slit Diffraction Analysis
Loads diffraction images for slit widths 0.2-0.8 mm, detects peak positions
using Gaussian smoothing and peak finding, computes the angular width of the
central diffraction maximum, and plots measured versus expected angular widths.
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
wavelength = 633e-9     # HeNe laser wavelength in metres

angleList = []

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
    plt.plot(x, midRowsAvg, label="Intensity Profile")

    peaks, _ = find_peaks(rowsSmooth, width=10, distance=150, height=4)

    if len(peaks) > 2:
        # Filter out 2nd-order and higher maxima to isolate the central pair
        centralMaxima = np.argmax(rowsSmooth[peaks])
        difference = peaks[centralMaxima + 1] - peaks[centralMaxima - 1]
    elif len(peaks) == 2:
        # If one outer maximum is out of frame, use center and available peak
        difference = (peaks[1] - peaks[0]) * 2
    else:
        difference = 0

    plt.plot(peaks, np.zeros(len(peaks)), "or", label="Detected Peaks")
    angularWidth = (meterPerPixel * difference) / L
    print(f"{slit / 10:.1f}mm : {angularWidth:.6f} Rads or {difference} pixels")
    angleList.append(angularWidth)

    plt.xlabel("Pixel Position")
    plt.ylabel("Pixel Intensity")
    plt.title(f"Diffraction Profile - Slit Width {slit / 10:.1f} mm")
    plt.savefig(f"{slit / 10:.1f}_profile.png")
    plt.show()
    plt.cla()

# Theoretical comparison plot
plt.figure()
plt.plot(slitRange / 10, angleList, label="Real Data")
expAngles = 2 * wavelength / (slitRange * 1e-4)  # 2*lambda / a
plt.plot(slitRange / 10, expAngles, label="Expected")
plt.xlabel("Slit Width (mm)")
plt.ylabel("Angular Width (Rads)")
plt.legend()
plt.title("Single-Slit Angular Divergence vs Slit Width")
plt.savefig("single_slit_angular_width.png")
plt.show()