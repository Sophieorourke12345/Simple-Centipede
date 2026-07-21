import pygame


class Centipede:
    def __init__(self, x, y, size, speed, colour):
        self.__start_x = x
        self.__start_y = y
        self.__rect = pygame.Rect(x, y, size, size)
        self.__speed = speed
        self.__colour = colour
        self.__direction = 1

    def draw(self, display):
        pygame.draw.rect(display, self.__colour, self.__rect)

    def move(self, dims):
        width, height = dims
        self.__rect.x += self.__speed * self.__direction

        if self.__rect.right >= width:
            self.__rect.right = width
            self.__direction = -1
            self.__rect.y += self.__rect.height
        elif self.__rect.left <= 0:
            self.__rect.left = 0
            self.__direction = 1
            self.__rect.y += self.__rect.height

        if self.__rect.centery > height / 2:
            self.relocate(dims)

    def relocate(self, dims):
        width, height = dims
        size = self.__rect.width

        self.__rect.x = min(max(self.__start_x, 0), width - size)
        self.__rect.y = min(max(self.__start_y, 0), height - size)
        self.__direction = 1

    def get_rect(self):
        return self.__rect

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_size(self):
        return self.__rect.size

    def get_speed(self):
        return self.__speed
