import pygame


class Dart:
    def __init__(self, width, height, colour, speed):
        self.__rect = pygame.Rect(0, 0, width, height)
        self.__colour = colour
        self.__speed = speed
        self.__active = False

    def __str__(self):
        return f"Dart(active={self.__active}, x={self.__rect.x}, y={self.__rect.y})"

    def fire_from(self, shooter_rect):
        if not self.__active:
            self.__rect.midbottom = shooter_rect.midtop
            self.__active = True

    def move(self, dims):
        if not self.__active:
            return

        self.__rect.y -= self.__speed

        if self.__rect.bottom < 0:
            self.__active = False

    def draw(self, display):
        if self.__active:
            pygame.draw.rect(display, self.__colour, self.__rect)

    def deactivate(self):
        self.__active = False

    def is_active(self):
        return self.__active

    def get_rect(self):
        return self.__rect

    def get_speed(self):
        return self.__speed
