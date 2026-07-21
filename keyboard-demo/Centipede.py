import pygame

class Centipede:
    """
    Represents a centipede segment that moves horizontally and drops down
    when hitting a wall. I encapsulate all movement rules inside this class
    so that the rest of the program does not need to know *how* the centipede
    behaves — only *when* to update or draw it.

    This strong encapsulation keeps main.py clean, but it also means that
    any extra behaviour added here affects all centipede movement. I chose
    this trade‑off intentionally because the game has only one centipede
    and its behaviour is simple and predictable.
    """

    def __init__(self, x, y, size, speed, colour):
        # Original spawn point — kept private so no external class can
        # accidentally reposition the centipede in a way that breaks logic.
        self.__start_x = x
        self.__start_y = y

        # Private rect ensures only Centipede controls its own movement.
        self.__rect = pygame.Rect(x, y, size, size)
        self.__speed = speed
        self.__colour = colour

        # Direction is internal state. I keep it private because exposing
        # it would allow other objects to flip direction unexpectedly.
        self.__direction = 1  # 1 = right, -1 = left

    def __str__(self):
        """Readable description for debugging."""
        return f"Centipede(colour={self.__colour}, x={self.__rect.x}, y={self.__rect.y})"

    def draw(self, display):
        """
        Draw the centipede. I keep drawing logic inside the class so that
        main.py does not need to know anything about pygame rectangles.
        """
        pygame.draw.rect(display, self.__colour, self.__rect)

    def move(self, dims):
        """
        Handles ALL movement behaviour for the centipede.

        I deliberately placed multiple behaviours inside this method:
        - horizontal movement
        - wall collision
        - dropping down
        - halfway reset

        This is a conscious design choice. In a larger game, mixing these
        behaviours in one method could make the class harder to extend or
        reuse. But for this assignment, the centipede has a very fixed,
        predictable pattern, so bundling the behaviours keeps the logic
        simple and readable.
        """
        width, height = dims

        # Horizontal movement based on speed and direction.
        self.__rect.x += self.__speed * self.__direction

        # --- Wall collision behaviour ---
        # I added the "drop down" behaviour directly inside the collision
        # checks. This tightly couples wall collision with vertical movement.
        #
        # This could be limiting if I wanted different centipede types with
        # different behaviours, but for this game it works perfectly because
        # the centipede always behaves the same way.
        if self.__rect.right >= width:
            self.__rect.right = width
            self.__direction = -1
            self.__rect.y += self.__rect.height  # drop down one row

        elif self.__rect.left <= 0:
            self.__rect.left = 0
            self.__direction = 1
            self.__rect.y += self.__rect.height

        # --- Halfway reset behaviour ---
        # I added this behaviour here instead of in main.py because the
        # centipede should be responsible for knowing when it has gone too far.
        #
        # This is another example of encapsulating behaviour that could be
        # limiting in a more complex game (e.g., multiple centipedes with
        # different thresholds), but for this assignment it keeps main.py
        # clean and centralises movement rules.
        reset_threshold = height / 2
        if self.__rect.centery > reset_threshold: #I initially had line 88 "height/2" in line 89, but i decided to create reset_threshold to make it cleaner and easier to read.
            self.relocate(dims)

    def relocate(self, dims):
        """
        Reset the centipede to its original spawn point.

        This method is called both internally (move()) and externally
        (main.py when the dart hits it). I encapsulate the reset logic here
        so that no other class needs to know how to reposition the centipede.

        This prevents bugs where external code might reset the centipede
        incorrectly or inconsistently.
        """
        width, height = dims
        size = self.__rect.width

        # Clamp starting position to ensure centipede always respawns on-screen.
        # This protects the object from invalid external parameters.
        x = min(max(self.__start_x, 0), width - size)
        y = min(max(self.__start_y, 0), height - size)

        self.__rect.x = x
        self.__rect.y = y

        # Reset direction so movement always restarts consistently.
        self.__direction = 1

    # -------------------------
    #        GETTERS
    # -------------------------
    # I intentionally provide only getters, not setters. This enforces
    # encapsulation: external classes can read state but cannot modify it.
    # This prevents accidental interference with movement logic.

    def get_x(self):
        return self.__rect.x

    def get_y(self):
        return self.__rect.y

    def get_size(self):
        return self.__rect.size

    def get_speed(self):
        return self.__speed

    def get_rect(self):
        """
        Returns the rect for collision detection.

        This is the ONLY part of the centipede's internal state that other
        objects (like Dart in main.py) are allowed to inspect.

        This controlled exposure is a deliberate OOP design choice: it allows
        interaction without giving external classes the ability to break
        movement behaviour.
        """
        return self.__rect
