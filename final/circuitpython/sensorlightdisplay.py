from adafruit_circuitplayground import cp
import time


class SensorLightDisplay:
    acceleration_peak = 9.81

    def __init__(self, brightness):
        self.pixels_off_state = (0, 0, 0)
        self.pixel_amount = len(cp.pixels)
        self.pixel_amount_half = self.pixel_amount // 2

        cp.pixels.brightness = brightness
        cp.pixels.auto_write = False

    def light(self, acceleration, colour):
        x = acceleration[0]
        cp.pixels.fill(self.pixels_off_state)

        if x < -1:
            for pixel in range(6, 9):
                cp.pixels[pixel] = colour
        elif x > 1:
            for pixel in range(1, 4):
                cp.pixels[pixel] = colour

        cp.pixels.show()
        time.sleep(0.1)

    def advanced_control_feedback(self, acceleration_x):
        x = acceleration_x

        if x < -9.81 or x > 9.81:
            return

        if -3 <= x <= 3:
            cp.pixels.fill((0, 0, 0))
            cp.pixels.show()
            return

        if x < -3:
            intensity = int(((abs(x) - 3) / (9.81 - 3)) * 235 + 20)
            cp.pixels.fill((intensity, 0, 0))
            cp.pixels.show()
            return

        leds_on = int(((x - 3) / (9.81 - 3)) * 9) + 1
        cp.pixels.fill((0, 0, 0))

        for i in range(leds_on):
            cp.pixels[i] = (0, 0, 255)

        cp.pixels.show()
