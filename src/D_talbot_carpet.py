"""
Appendix D: 2D Carpet Analysis with Vertical and Horizontal Peak Finding
Iterates over longitudinal camera distances, isolates the vertical center of
the diffraction pattern, extracts horizontal intensity bands, and concatenates
them into a 2D Talbot carpet array for near-field visualization.
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

x = np.arange(0, 1280, 1)
y = np.arange(0, 1024, 1)
colNum = 1024           # column span for vertical profile averaging
meterPerPixel = 5.2e-6  # size of pixel in metres
LRange = np.arange(30, 155, 5)  # distance from grating to camera (mm)

verticalMidpoints = []
horizontalMidpoints = []
carpet_bands = []

for L in LRange:
    filename = f"{L}mm.png"
    im = Image.open(filename).convert('L')
    na = np.array(im)

    # Vertical profile integration to find pattern centroid
    col_profile = np.average(
        na[(na.shape[0] // 2 - colNum // 2):(na.shape[0] // 2 + colNum // 2), :],
        axis=1
    )
    colsSmooth = gaussian_filter1d(col_profile, sigma=3)
    peaks, _ = find_peaks(colsSmooth, width=10, distance=100, height=4)

    if len(peaks) > 0:
        central_y_idx = peaks[np.argmax(colsSmooth[peaks])]
    else:
        central_y_idx = na.shape[0] // 2

    verticalMidpoints.append(central_y_idx)

    # Extract 8-pixel horizontal band centered on beam centroid
    PixelBand = na[central_y_idx - 4:central_y_idx + 4, :]
    carpet_bands.append(PixelBand)

    midRowsAvg = np.average(PixelBand, axis=0)
    rowsSmooth = gaussian_filter1d(midRowsAvg, sigma=3)

    hpeaks, _ = find_peaks(rowsSmooth, width=10, distance=100, height=4)
    if len(hpeaks) > 0:
        central_x_idx = hpeaks[np.argmax(rowsSmooth[hpeaks])]
        horizontalMidpoints.append(central_x_idx)

# Concatenate stacked bands into 2D Talbot Carpet
carpet = np.concatenate(carpet_bands, axis=0)

plt.figure(figsize=(10, 6))
# Transpose or display with extent matching physical dimensions
plt.imshow(carpet, cmap='hot', aspect='auto')
plt.colorbar(label="Normalised Intensity")
plt.xlabel("Transverse Position Along Sensor (Pixels)")
plt.ylabel("Longitudinal Translation Index (z-sweep)")
plt.title("Reconstructed Near-Field Talbot Carpet")
plt.savefig("talbot_carpet_reconstruction.png")
plt.show()