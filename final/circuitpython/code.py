from adafruit_circuitplayground import cp
from sensorlightdisplay import SensorLightDisplay
import time

# ---------------------------------------------------------
# BASE REQUIREMENTS VERSION OF CODE.PY
# ---------------------------------------------------------
# This version:
# - Reads accelerometer (x, y, z)
# - Reads button A and B
# - Provides simple tilt feedback using SensorLightDisplay.light()
# - Prints values over serial for Pygame to read
# ---------------------------------------------------------

# Create SensorLightDisplay object for LED feedback
display = SensorLightDisplay(brightness=0.3)

while True:
    # Read buttons
    a = cp.button_a
    b = cp.button_b

    # Read accelerometer values
    x, y, z = cp.acceleration

    # -----------------------------------------------------
    # BASE LED FEEDBACK (Assignment Requirement)
    # Uses your existing tilt-based light() method
    # -----------------------------------------------------
    #display.advanced_control_feedback(x)
    display.light((x, y, z), (0, 0, 255))



    # -----------------------------------------------------
    # SERIAL OUTPUT FOR PYGAME
    # Pygame will read this line and split it into values
    # -----------------------------------------------------
    print(f"{a},{b},{x:.2f},{y:.2f},{z:.2f}")

    time.sleep(0.01)
