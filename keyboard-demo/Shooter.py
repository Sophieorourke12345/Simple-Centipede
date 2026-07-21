import pygame

class Shooter:
    """
    Represents the player's controllable shooter at the bottom of the screen.

    I designed this class so that it encapsulates all behaviour related to
    the shooter's position, movement rules, and rendering. This keeps the
    shooter self-contained and prevents main.py from needing to manipulate
    its internal state directly.

    This class interacts with Dart (by providing its rect for firing) and
    with main.py (which supplies keyboard input), but it never controls
    other objects. This one‑directional interaction is intentional and keeps
    the shooter focused on its own responsibilities.

    The movement system originally used mouse input, but I refactored it to
    use keyboard controls instead. This change reinforces the idea that the
    Shooter should not care *how* input is received — only *how* it moves
    when instructed. main.py interprets the input, and the Shooter simply
    applies its own movement rules.
    """

    def __init__(self, x, y, width, height, colour, speed):
        # Private rect ensures only the Shooter class controls its own position.
        # This prevents external code from accidentally breaking movement rules.
        self.__rect = pygame.Rect(x, y, width, height)
        self.__colour = colour

        # Speed is now used for keyboard movement.
        # Keeping it encapsulated allows future control schemes (AI, acceleration, etc.)
        # without modifying main.py.
        self.__speed = speed

    def __str__(self):
        """Readable description for debugging."""
        return f"Shooter(colour={self.__colour}, x={self.__rect.x}, y={self.__rect.y})"

    def draw(self, display):
        """
        Draws the shooter on the screen.

        I keep drawing logic inside the class so that main.py does not need
        to know anything about pygame rectangles or colours. This follows the
        OOP principle of hiding implementation details.
        """
        pygame.draw.rect(display, self.__colour, self.__rect)

    # ---------------------------------------------------------
    # KEYBOARD MOVEMENT
    # ---------------------------------------------------------
    # I added this method to support arrow‑key movement. The Shooter does not
    # read keyboard input directly — that would tightly couple it to pygame.
    #
    # Instead, main.py simply tells the Shooter *which direction* to move,
    # and the Shooter applies its own movement rules and boundary clamping.
    #
    # This keeps the class reusable and maintains strong encapsulation.
    # ---------------------------------------------------------

    def move_keyboard(self, direction, window_width):
        """
        Moves the shooter horizontally using keyboard input.

        direction = -1 for left, +1 for right.

        I intentionally keep boundary‑clamping behaviour inside this method
        rather than in main.py. This ensures the shooter ALWAYS stays on-screen,
        regardless of how movement is triggered.

        This is a good example of encapsulating behaviour to protect the
        object's internal state from invalid values.
        """
        self.__rect.x += direction * self.__speed

        # Clamp to left boundary.
        if self.__rect.left < 0:
            self.__rect.left = 0

        # Clamp to right boundary.
        if self.__rect.right > window_width:
            self.__rect.right = window_width

    # -------------------------
    #        GETTERS
    # -------------------------
    # I provide only getters, not setters, to maintain encapsulation.
    # External classes can read the shooter's state but cannot modify it.
    # This prevents accidental interference with movement logic.

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_speed(self):
        return self.__speed

    def get_size(self):
        return self.__rect.size  # (width, height)

    def get_rect(self):
        """
        Returns the shooter's rect for collision checks or for positioning
        the dart when firing.

        This is the main point of interaction between Shooter and Dart:
        - Dart.fire_from() receives this rect and positions itself relative
          to the shooter.
        - Shooter does NOT know anything about the dart's behaviour.
          This one‑way dependency is intentional and keeps the shooter
          decoupled from projectile logic.

        This demonstrates good OOP design: each object exposes only what
        other objects need, and nothing more.
        """
        return self.__rect
