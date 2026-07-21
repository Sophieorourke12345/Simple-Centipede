import pygame
import sys
import serial
from shooter import Shooter
from centipede import Centipede
from dart import Dart
from eventlist import EventList


pygame.init()
ser = serial.Serial('/dev/tty.usbmodem141101', 115200)


def read_cpe():
    try:
        line = ser.readline().decode().strip()
        a, b, x, y, z = line.split(',')
        return (a == "True"), (b == "True"), float(x), float(y), float(z)
    except Exception:
        return False, False, 0, 0, 0


WIDTH, HEIGHT = 800, 600
dims = [WIDTH, HEIGHT]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede Game - CPX Controlled")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

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
round_hits = 0
round_number = 1
running = True
last_direction = "neutral"

while running:
    screen.fill((0, 0, 0))

    a, b, x, y, z = read_cpe()
    direction = "neutral"

    if x < -3:
        shooter.move_keyboard(-1, WIDTH)
        direction = "left"
    elif x > 3:
        shooter.move_keyboard(1, WIDTH)
        direction = "right"

    if direction != last_direction:
        if direction == "left":
            event_list.add_event("Shooter moved left")
        elif direction == "right":
            event_list.add_event("Shooter moved right")
        else:
            event_list.add_event("Shooter stopped")
        last_direction = direction

    if a:
        dart.fire_from(shooter.get_rect())
        event_list.add_event("Dart fired")

    if b:
        dart.deactivate()
        event_list.add_event("Dart cancelled")

    centipede.move(dims)
    dart.move(dims)

    if dart.is_active() and dart.get_rect().colliderect(centipede.get_rect()):
        dart.deactivate()
        centipede.relocate(dims)
        round_hits += 1
        event_list.add_event("Centipede hit")

    if round_hits >= 3:
        round_number += 1
        round_hits = 0
        centipede.relocate(dims)
        dart.deactivate()
        event_list.add_event(f"Round {round_number} started")

    shooter.draw(screen)
    centipede.draw(screen)
    dart.draw(screen)

    info = font.render(f"Round: {round_number} | Hits: {round_hits}/3", True, (255, 255, 255))
    screen.blit(info, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

print("Event List")
event_list.print_events()

pygame.quit()
sys.exit()
