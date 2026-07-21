import pygame
import sys
import serial
from shooter import Shooter
from centipede import Centipede
from dart import Dart
from eventlist import EventList

pygame.init()

# -----------------------------
# Connecting to the CPX (serial)
# -----------------------------
# I read data from the Circuit Playground Express so the game can be controlled
# using real hardware (buttons + accelerometer). This shows how software and
# hardware can interact together.
ser = serial.Serial('/dev/tty.usbmodem141101', 115200)

def read_cpe():
    """
    Reads a line of serial data from the CPX.
    I return booleans for button A/B and floats for the accelerometer.
    Keeping this in a function avoids repeating serial‑parsing code.
    """
    try:
        line = ser.readline().decode().strip()
        a, b, x, y, z = line.split(',')
        return (a == "True"), (b == "True"), float(x), float(y), float(z)
    except:
        return False, False, 0, 0, 0


# -----------------------------
# Window + game setup
# -----------------------------
WIDTH, HEIGHT = 800, 600
dims = [WIDTH, HEIGHT]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede Game - CPE Controlled")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


# -----------------------------
# Creating game objects (OOP)
# -----------------------------
# Each object comes from its own class. This shows OOP in action:
# - Shooter handles player movement + drawing
# - Centipede handles enemy movement + resetting
# - Dart handles projectile behaviour
# - EventList stores a history of actions
#
# Using classes keeps the code organised and avoids repeating logic.
shooter = Shooter(
    x=WIDTH // 2 - 25,
    y=HEIGHT - 60,
    width=50,
    height=30,
    colour=(0, 0, 255),
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

event_list = EventList()


# -----------------------------
# Game state variables
# -----------------------------
round_hits = 0
round_number = 1
max_rounds = 3
running = True
last_direction = "neutral"


# -----------------------------
# Main game loop
# -----------------------------
# This loop runs the entire game. I only use ONE while loop because Python
# cannot multitask between multiple infinite loops. Everything updates inside
# this loop: input, movement, collisions, drawing, and UI.
while running:
    screen.fill((0, 0, 0))

    # Read input from the CPX
    a, b, x, y, z = read_cpe()


    # -------------------------
    # Moving the shooter (tilt)
    # -------------------------
    # I use the accelerometer's X value to move left/right.
    # This shows how hardware input can control a software object.
    direction = "neutral"

    if x < -3:
        shooter.move_keyboard(-1, WIDTH)
        direction = "left"

    elif x > 3:
        shooter.move_keyboard(1, WIDTH)
        direction = "right"

    # Log direction changes only when they actually change
    if direction != last_direction:
        if direction == "left":
            event_list.add_event("Shooter moved left")
        elif direction == "right":
            event_list.add_event("Shooter moved right")
        else:
            event_list.add_event("Shooter stopped")

        last_direction = direction


    # -------------------------
    # Dart control (buttons)
    # -------------------------
    # Button A fires the dart.
    # Button B cancels it.
    # This shows how the Dart class encapsulates its own behaviour.
    if a:
        dart.fire_from(shooter.get_rect())
        event_list.add_event("Dart fired")

    if b:
        dart.deactivate()
        event_list.add_event("Dart cancelled")


    # -------------------------
    # Updating game objects
    # -------------------------
    # Each object updates itself using its own methods.
    # This is classic OOP: each class handles its own behaviour.
    centipede.move(dims)
    dart.move(dims)


    # -------------------------
    # Collision detection
    # -------------------------
    # I check if the dart hits the centipede using pygame's built‑in
    # rectangle collision. If they collide, I reset the centipede and
    # deactivate the dart.
    if dart.is_active() and dart.get_rect().colliderect(centipede.get_rect()):
        dart.deactivate()
        centipede.relocate(dims)
        round_hits += 1
        event_list.add_event("Centipede hit")


    # -------------------------
    # Round progression
    # -------------------------
    # Every 3 hits, the round increases and the centipede resets.
    if round_hits >= 3:
        round_number += 1
        round_hits = 0
        centipede.relocate(dims)
        dart.deactivate()
        event_list.add_event(f"Round {round_number} started")


    # -------------------------
    # Drawing everything
    # -------------------------
    shooter.draw(screen)
    centipede.draw(screen)
    dart.draw(screen)


    # -------------------------
    # UI text (round + hits)
    # -------------------------
    info = font.render(f"Round: {round_number} | Hits: {round_hits}/3", True, (255, 255, 255))
    screen.blit(info, (10, 10))


    # -------------------------
    # Quit event
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)


# -----------------------------
# Print event history on exit
# -----------------------------
print("\n--- Event List ---")
event_list.print_events()

pygame.quit()
sys.exit()
