import pygame


class Shooter:
    def __init__(self, x, y, width, height, colour, speed):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__colour = colour
        self.__speed = speed

    def draw(self, display):
        pygame.draw.rect(display, self.__colour, self.__rect)

    def move_keyboard(self, direction, window_width):
        self.__rect.x += direction * self.__speed

        if self.__rect.left < 0:
            self.__rect.left = 0
        if self.__rect.right > window_width:
            self.__rect.right = window_width

    def get_rect(self):
        return self.__rect

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_speed(self):
        return self.__speed
