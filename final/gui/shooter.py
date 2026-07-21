import pygame

class Shooter:
    """
    Represents the player's controllable shooter at the bottom of the screen.
    The Shooter does not read input directly — main.py controls WHEN it moves.
    This class only controls HOW it moves.
    """

    def __init__(self, x, y, width, height, colour, speed):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__colour = colour
        self.__speed = speed

    def draw(self, display):
        pygame.draw.rect(display, self.__colour, self.__rect)

    def move_keyboard(self, direction, window_width):
        """
        Moves horizontally only.
        direction = -1 (left), +1 (right)
        """
        self.__rect.x += direction * self.__speed

        # boundary clamp
        if self.__rect.left < 0:
            self.__rect.left = 0
        if self.__rect.right > window_width:
            self.__rect.right = window_width

    # -------- GETTERS --------
    def get_rect(self):
        return self.__rect

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_speed(self):
        return self.__speed
