import pygame

class Dart:
    """
    This class represents a projectile fired by the Shooter.
    I used a class because it lets me bundle together all the data
    (position, size, speed, active state) and all the behaviour
    (firing, moving, drawing, deactivating) into one organised unit.

    This shows encapsulation: the Dart object controls its own state
    and exposes only the methods I want other parts of the game to use.
    """

    def __init__(self, width, height, colour, speed):
        """
        The constructor sets up the dart's initial state.
        I use private attributes (with __) to protect the internal data.
        This prevents other parts of the program from accidentally changing
        the dart's state, which is a key part of encapsulation.
        """

        # The dart is represented by a pygame.Rect for easy movement and collision.
        self.__rect = pygame.Rect(0, 0, width, height)

        # Store the colour so draw() can use it.
        self.__colour = colour

        # Speed controls how fast the dart moves upward.
        self.__speed = speed

        # The dart starts inactive so it doesn't appear until fired.
        self.__active = False

    def fire_from(self, shooter_rect):
        """
        This method activates the dart and positions it at the top of the shooter.
        I keep this logic inside the class so I don't repeat code anywhere else.
        This also shows good method design: one method = one responsibility.
        """

        # Only fire if the dart is not already active.
        if not self.__active:
            # Position the dart so it appears to come out of the shooter.
            self.__rect.midbottom = shooter_rect.midtop
            self.__active = True

    def move(self, dims):
        """
        This method moves the dart upward while it is active.
        I separate movement logic into its own method so it can be reused
        every frame without repeating code.
        """

        # If the dart isn't active, there is nothing to move.
        if not self.__active:
            return

        # Move upward by subtracting speed from the y‑position.
        self.__rect.y -= self.__speed

        # If the dart goes off the top of the screen, deactivate it.
        if self.__rect.bottom < 0:
            self.__active = False

    def draw(self, display):
        """
        This method draws the dart only when it is active.
        I keep drawing logic inside the class so the object controls
        how it appears — another example of encapsulation.
        """

        if self.__active:
            pygame.draw.rect(display, self.__colour, self.__rect)

    def deactivate(self):
        """
        This method turns the dart off.
        I created a separate method for this so other parts of the game
        can deactivate the dart without touching internal attributes.
        This is controlled access, which is good OOP practice.
        """
        self.__active = False

    # -------------------------
    # GETTERS (controlled access)
    # -------------------------
    # I use getters instead of exposing attributes directly.
    # This protects the internal state and shows encapsulation.
    # If I ever change how the dart stores its data,
    # the rest of the game won't break because they only use these methods.

    def is_active(self):
        return self.__active

    def get_rect(self):
        return self.__rect
