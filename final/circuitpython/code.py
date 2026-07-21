from adafruit_circuitplayground import cp
from sensorlightdisplay import SensorLightDisplay
import time


display = SensorLightDisplay(brightness=0.3)

while True:
    a = cp.button_a
    b = cp.button_b
    x, y, z = cp.acceleration

    display.light((x, y, z), (0, 0, 255))
    print(f"{a},{b},{x:.2f},{y:.2f},{z:.2f}")

    time.sleep(0.01)
