import pygame
import sys
from Shooter import Shooter
from Centipede import Centipede
from Dart import Dart

pygame.init()

# ---------------------------------------------------------
# Hi Laura, I wanted to include a few general comments to better explain the
# overall design approach I took for this object‑oriented programming assignment.
#
# The classes in my game follow a simple, one‑directional relationship structure:
#
# - Shooter → provides its rect to Dart when firing.
# - Dart → interacts with Centipede only through collision checks in main.py.
# - Centipede → has no knowledge of Shooter or Dart.
# - main.py → orchestrates all interactions.
#
# This prevents circular dependencies and keeps each class reusable and focused
# on its own behaviour.
#
# Game rules such as scoring, rounds, and win conditions stay in main.py because
# they represent higher‑level game logic, not object behaviour. Keeping this logic
# out of the classes ensures they remain reusable in other games and prevents them
# from becoming tightly coupled to this specific Centipede project.
#
# The game currently uses a single dart and a single centipede. This keeps the
# design simple and easy to manage, but the architecture could be extended in
# future versions by using lists of objects or inheritance for different enemy
# types.
#
# Some ideas for future improvements include:
#
# - Multiple darts using a list of projectiles.
# - Multiple centipede segments using composition.
# - Keyboard controls using a movement strategy pattern.
# - Sound effects and animations.
#
# ----------------------------------------------------------
# SELF‑LEARNED CONCEPTS USED IN THIS PROJECT
# ----------------------------------------------------------
# Throughout this project I applied several concepts that I researched and
# learned independently:
#
# - Effective use of pygame.Rect for collision, movement, and alignment.
# - Event‑driven programming to control object behaviour using input.
# - Encapsulation to protect internal state inside each class.
# - One‑way dependencies (Shooter → Dart, main → objects) to avoid tight coupling.
# - Composition: the game is built from independent objects that interact only
#   through controlled methods.
#
# Applying these concepts helped me design a cleaner, more modular architecture
# and gave me a better understanding of how real games structure their logic.
# ---------------------------------------------------------


# Window dimensions are stored in variables so they can be passed to objects.
# This avoids hard‑coding values inside classes, keeping them reusable.
WIDTH, HEIGHT = 800, 600
dims = [WIDTH, HEIGHT]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede Game - OOP Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


# ---------------------------------------------------------
# OBJECT CREATION
# ---------------------------------------------------------
# I instantiate each object here because main.py is responsible for
# orchestrating the game. Each class handles its own behaviour, but
# main.py decides WHEN those behaviours should run.
#
# This follows the OOP principle of "composition":
# the game is composed of interacting objects, each with a clear role.
# ---------------------------------------------------------

shooter = Shooter(
    x=WIDTH // 2 - 25,
    y=HEIGHT - 60,
    width=50,
    height=30,
    colour=(0, 0, 255),
    # Speed is now used for keyboard movement. I keep it here so that
    # movement rules remain encapsulated inside the Shooter class.
    speed=6
)

centipede = Centipede(
    x=0,
    y=50,
    size=40,
    speed=4,
    colour=(0, 255, 0)
)

dart = Dart(
    width=5,
    height=15,
    colour=(255, 0, 0),
    speed=10
)

# ---------------------------------------------------------
# GAME STATE VARIABLES
# ---------------------------------------------------------
# These variables belong in main.py because they represent game logic,
# not object behaviour. The objects themselves should not know anything
# about rounds, scoring, or progression.
#
# This separation of concerns is intentional: objects handle behaviour,
# main.py handles rules.
# ---------------------------------------------------------

round_hits = 0
round_number = 1
max_rounds = 3

running = True

# ---------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------
# This loop is the "director" of the game. It does not implement
# movement or drawing logic itself — it simply tells each object
# when to update and when to render.
#
# This is a classic OOP game architecture:
# - main.py = orchestrator
# - objects = behaviour owners
# ---------------------------------------------------------

while running:
    screen.fill((0, 0, 0))

    # -----------------------------------------------------
    # EVENT HANDLING
    # -----------------------------------------------------
    # I keep event handling in main.py because events represent
    # player input, not object behaviour. Objects should not
    # directly read keyboard input — that would tightly couple
    # them to pygame.
    #
    # Instead, main.py interprets input and then calls methods
    # on the objects, which decide how to respond.
    # -----------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard events control firing and cancelling the dart.
        # This is an example of controlled interaction:
        # main.py triggers the action, but Dart decides how to behave.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spacebar fires the dart from the shooter.
                dart.fire_from(shooter.get_rect())
            elif event.key == pygame.K_z:
                # Z cancels the current shot by deactivating the dart.
                dart.deactivate()

    # -----------------------------------------------------
    # CONTINUOUS KEYBOARD MOVEMENT
    # -----------------------------------------------------
    # I use pygame.key.get_pressed() outside the event loop so that
    # holding down the arrow keys results in smooth, continuous movement.
    #
    # main.py only decides the direction (-1 or +1). The Shooter class
    # encapsulates the actual movement rules and boundary clamping.
    # -----------------------------------------------------

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shooter.move_keyboard(-1, WIDTH)
    if keys[pygame.K_RIGHT]:
        shooter.move_keyboard(1, WIDTH)

    # -----------------------------------------------------
    # UPDATE GAME OBJECTS
    # -----------------------------------------------------
    # Each object updates itself. main.py does not modify internal
    # attributes directly — this respects encapsulation.
    # -----------------------------------------------------

    centipede.move(dims)
    dart.move(dims)

    # -----------------------------------------------------
    # COLLISION DETECTION
    # -----------------------------------------------------
    # Collision logic belongs in main.py because it involves
    # interaction BETWEEN objects, not behaviour OF objects.
    #
    # Neither Dart nor Centipede should be responsible for knowing
    # about each other — that would violate encapsulation.
    # -----------------------------------------------------

    if dart.is_active() and dart.get_rect().colliderect(centipede.get_rect()):
        dart.deactivate()
        centipede.relocate(dims)
        round_hits += 1

    # -----------------------------------------------------
    # ROUND / GAME LOGIC
    # -----------------------------------------------------
    # This logic stays in main.py because it represents game rules,
    # not object behaviour. Objects should not know about scoring.
    #
    # This separation keeps classes reusable in other games.
    # -----------------------------------------------------

    if round_hits >= 3:
        round_number += 1
        round_hits = 0

        # Reset objects for next round.
        centipede.relocate(dims)
        dart.deactivate()

        # End game after max rounds.
        if round_number > max_rounds:
            running = False

    # -----------------------------------------------------
    # DRAW OBJECTS
    # -----------------------------------------------------
    # Each object draws itself. main.py does not know HOW they draw,
    # only that they have a draw() method.
    #
    # This is polymorphism in practice: any object with a draw()
    # method could be added here without changing the game loop.
    # -----------------------------------------------------

    shooter.draw(screen)
    centipede.draw(screen)
    dart.draw(screen)
    # The game loop treats all objects polymorphically by calling draw() on
    # each one. Any new object with a draw() method could be added without
    # changing the loop, demonstrating polymorphism in practice.

    # -----------------------------------------------------
    # UI / TEXT
    # -----------------------------------------------------
    # UI is not part of any object's responsibility.
    # It belongs in main.py because it represents game state.
    # -----------------------------------------------------

    info = font.render(f"Round: {round_number} | Hits: {round_hits}/3", True, (255, 255, 255))
    screen.blit(info, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
