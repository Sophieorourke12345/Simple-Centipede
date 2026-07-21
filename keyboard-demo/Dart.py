import pygame

class Dart:
    """
    Represents a projectile fired by the Shooter.

    I encapsulate all dart behaviour inside this class so that main.py does not
    need to manage projectile physics, activation rules, or screen boundaries.
    This keeps the game loop clean and prevents bugs caused by external code
    modifying the dart's state incorrectly.

    The dart does not read keyboard or mouse input directly. Instead, main.py
    decides WHEN the dart should activate (Space key) or deactivate (Z key),
    and the Dart class decides HOW to behave in response. This separation keeps
    the class reusable and prevents it from becoming tightly coupled to any
    specific control scheme.
    """

    def __init__(self, width, height, colour, speed):
        # The dart starts off-screen and inactive.
        # I keep the rect private so only the Dart class controls its position.
        self.__rect = pygame.Rect(0, 0, width, height)
        self.__colour = colour
        self.__speed = speed

        # Active state determines whether the dart should move or draw.
        # This is private because external classes should not toggle it
        # except through fire_from() or deactivate().
        self.__active = False

    def __str__(self):
        """Readable description for debugging."""
        return f"Dart(active={self.__active}, x={self.__rect.x}, y={self.__rect.y})"

    def fire_from(self, shooter_rect):
        """
        Activates the dart and positions it at the top of the shooter.

        I intentionally added the rule "only fire if inactive" here.
        This behaviour prevents rapid-fire spamming and ensures only one dart
        exists at a time. This is a design choice that simplifies gameplay.

        main.py now triggers this method when the player presses the SPACE key.
        The Dart class does not care *which* key was pressed — it only cares
        that it has been instructed to activate. This keeps input logic
        separate from projectile behaviour.
        """
        if not self.__active:
            self.__rect.midbottom = shooter_rect.midtop
            self.__active = True

    def move(self, dims):
        """
        Moves the dart vertically upwards.

        I placed the "deactivate when leaving screen" behaviour inside this
        method because the dart should manage its own lifecycle.

        This method is called every frame, but the dart only moves when active.
        """
        if not self.__active:
            return

        width, height = dims
        self.__rect.y -= self.__speed

        # If the dart leaves the screen, deactivate it.
        if self.__rect.bottom < 0:
            self.__active = False

    def draw(self, display):
        """
        Draws the dart only when active.

        I intentionally put the active check here instead of in main.py.
        This keeps drawing logic encapsulated and prevents main.py from needing
        to know the dart's internal state.
        """
        if self.__active:
            pygame.draw.rect(display, self.__colour, self.__rect)

    def deactivate(self):
        """
        Deactivates the dart, typically after a collision or when the player
        manually cancels the shot.

        main.py now calls this method when the player presses the Z key.
        This gives the player control over cancelling a shot, but the Dart
        class still manages the actual state change. This maintains strong
        encapsulation: main.py requests the change, and the Dart object
        decides how to apply it.
        """
        self.__active = False

    # --- Getters ---

    def is_active(self):
        """Returns whether the dart is currently active."""
        return self.__active

    def get_rect(self):
        """Returns the rect for collision detection."""
        return self.__rect

    def get_speed(self):
        """Return dart speed (read-only)."""
        return self.__speed
