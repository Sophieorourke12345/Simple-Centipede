import pygame

class Centipede:
    """
    This class represents a single centipede segment in the game.
    I used a class because it allows me to bundle together all the data
    (position, speed, colour, direction) and all the behaviour
    (drawing, moving, relocating) into one organised unit.

    This shows encapsulation: the object controls its own state and
    exposes only the methods I want other parts of the program to use.
    """

    def __init__(self, x, y, size, speed, colour):
        """
        The constructor sets up the initial state of the centipede segment.
        I use private attributes (with __) to protect the internal data.
        This means other code cannot accidentally change these values directly,
        which is a key part of encapsulation in OOP.
        """

        # I store the starting position so I can reset the centipede later.
        self.__start_x = x
        self.__start_y = y

        # I use a pygame.Rect to represent the centipede's position and size.
        # This keeps the code clean and lets me use built‑in collision features.
        self.__rect = pygame.Rect(x, y, size, size)

        # Speed controls how fast the centipede moves horizontally.
        self.__speed = speed

        # The colour is stored so the draw() method can use it.
        self.__colour = colour

        # Direction: 1 means moving right, -1 means moving left.
        # I store this as an attribute so the centipede can change direction
        # when it hits a wall.
        self.__direction = 1

    def draw(self, display):
        """
        This method draws the centipede segment on the screen.
        I keep drawing logic inside the class so the object is responsible
        for how it appears — another example of encapsulation.
        """
        pygame.draw.rect(display, self.__colour, self.__rect)

    def move(self, dims):
        """
        This method handles all movement logic.
        It updates the x‑position, checks for wall collisions,
        changes direction, and drops the centipede down a row.

        By putting this behaviour inside a method, I avoid repeating
        movement code anywhere else in the program.
        """

        width, height = dims

        # Move horizontally based on speed and direction.
        self.__rect.x += self.__speed * self.__direction

        # If the centipede hits the right wall:
        if self.__rect.right >= width:
            # Snap to the wall so it doesn't go off‑screen.
            self.__rect.right = width

            # Reverse direction.
            self.__direction = -1

            # Drop down one row (classic centipede behaviour).
            self.__rect.y += self.__rect.height

        # If the centipede hits the left wall:
        elif self.__rect.left <= 0:
            self.__rect.left = 0
            self.__direction = 1
            self.__rect.y += self.__rect.height

        # If the centipede reaches halfway down the screen,
        # I reset it to its starting position.
        # This prevents it from disappearing off‑screen.
        if self.__rect.centery > height / 2:
            self.relocate(dims)

    def relocate(self, dims):
        """
        This method resets the centipede to its original starting position.
        I keep this logic separate so it can be reused whenever needed.
        This shows good method design and avoids repeating code.
        """

        width, height = dims
        size = self.__rect.width

        # Reset to starting x/y, but clamp inside the screen boundaries.
        self.__rect.x = min(max(self.__start_x, 0), width - size)
        self.__rect.y = min(max(self.__start_y, 0), height - size)

        # Reset direction to moving right.
        self.__direction = 1

    # -------------------------
    # GETTERS (controlled access)
    # -------------------------
    # I use getters instead of exposing attributes directly.
    # This is part of encapsulation: I control how other code interacts
    # with the internal state of the object.

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
