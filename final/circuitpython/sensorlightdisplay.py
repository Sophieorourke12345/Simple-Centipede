from adafruit_circuitplayground import cp
import time

class SensorLightDisplay:
    """
    Provides LED feedback based on accelerometer values.
    Includes:
    - Basic tilt feedback (Assignment Base Requirement)
    - Advanced feedback (Feature 2)
    """

    # Class variable
    acceleration_peak = 9.81

    def __init__(self, brightness):
        self.pixels_off_state = (0, 0, 0)
        self.pixel_amount = len(cp.pixels)
        self.pixel_amount_half = self.pixel_amount // 2

        cp.pixels.brightness = brightness
        cp.pixels.auto_write = False

    # ---------------------------------------------------------
    # BASE REQUIREMENT FEEDBACK (Assignment 2 style)
    # ---------------------------------------------------------
    def light(self, acceleration, colour):
        """
        Simple left/right tilt feedback.
        Lights left or right side depending on x tilt.
        """
        x = acceleration[0]

        cp.pixels.fill(self.pixels_off_state)

        if x < -1:
            # left tilt → light left side
            for pixel in range(6, 9):
                cp.pixels[pixel] = colour

        elif x > 1:
            # right tilt → light right side
            for pixel in range(1, 4):
                cp.pixels[pixel] = colour

        cp.pixels.show()
        time.sleep(0.1)

    # ---------------------------------------------------------
    # FEATURE 2: ADVANCED CONTROL FEEDBACK
    # ---------------------------------------------------------

    def advanced_control_feedback(self, acceleration_x):
        """
        Provides advanced LED feedback based on x-tilt.
        - If x < -3: colour intensity mapped to tilt (red gradient)
        - If x > 3: number of LEDs lit mapped to tilt
        - If -3 <= x <= 3: LEDs off
        """

        x = acceleration_x

        # Only run if within valid range
        if x < -9.81 or x > 9.81:
            return

        # -----------------------------
        # NEUTRAL ZONE: LEDs OFF
        # -----------------------------
        if -3 <= x <= 3:
            cp.pixels.fill((0, 0, 0))
            cp.pixels.show()
            return

        # -----------------------------
        # PATTERN A: x < -3
        # Colour intensity mapped to tilt
        # -----------------------------
        if x < -3:
            # Map tilt (-3 to -9.81) → intensity (20 to 255)
            intensity = int(((abs(x) - 3) / (9.81 - 3)) * 235 + 20)
            colour = (intensity, 0, 0)  # red gradient

            cp.pixels.fill(colour)
            cp.pixels.show()
            return

        # -----------------------------
        # PATTERN B: x > 3
        # Number of LEDs lit mapped to tilt
        # -----------------------------
        if x > 3:
            # Map tilt (3 to 9.81) → LEDs (1 to 10)
            leds_on = int(((x - 3) / (9.81 - 3)) * 9) + 1

            cp.pixels.fill((0, 0, 0))
            for i in range(leds_on):
                cp.pixels[i] = (0, 0, 255)  # blue LEDs
            cp.pixels.show()
            return
