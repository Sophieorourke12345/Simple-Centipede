import pygame
import sys
from Shooter import Shooter
from Centipede import Centipede
from Dart import Dart


pygame.init()

WIDTH, HEIGHT = 800, 600
dims = [WIDTH, HEIGHT]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede Game - Keyboard Demo")
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

round_hits = 0
round_number = 1
max_rounds = 3
running = True

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dart.fire_from(shooter.get_rect())
            elif event.key == pygame.K_z:
                dart.deactivate()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shooter.move_keyboard(-1, WIDTH)
    if keys[pygame.K_RIGHT]:
        shooter.move_keyboard(1, WIDTH)

    centipede.move(dims)
    dart.move(dims)

    if dart.is_active() and dart.get_rect().colliderect(centipede.get_rect()):
        dart.deactivate()
        centipede.relocate(dims)
        round_hits += 1

    if round_hits >= 3:
        round_number += 1
        round_hits = 0
        centipede.relocate(dims)
        dart.deactivate()

        if round_number > max_rounds:
            running = False

    shooter.draw(screen)
    centipede.draw(screen)
    dart.draw(screen)

    info = font.render(f"Round: {round_number} | Hits: {round_hits}/3", True, (255, 255, 255))
    screen.blit(info, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
