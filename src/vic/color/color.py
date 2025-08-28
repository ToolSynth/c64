import numpy as np

# Precomputed RGB values for the 16 C64 colors.
COLORS: np.ndarray = np.array(
    [
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (136, 0, 0),  # Red
        (170, 255, 238),  # Cyan
        (204, 68, 204),  # Purple
        (0, 204, 85),  # Green
        (0, 0, 170),  # Blue
        (238, 238, 119),  # Yellow
        (221, 136, 85),  # Orange
        (102, 68, 0),  # Brown
        (255, 119, 119),  # Light Red
        (51, 51, 51),  # Dark Grey
        (119, 119, 119),  # Grey
        (170, 255, 102),  # Light Green
        (0, 136, 255),  # Light Blue
        (187, 187, 187),  # Light Grey
    ],
    dtype=np.uint8,
)
