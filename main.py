import pygame
import sys
from player import *
from constants import *
from asteroidfield import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    time_clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    asteroidfield = AsteroidField()
    my_player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        for asteroid in asteroids:
            if my_player.collision_check(asteroid):
                print("Game Over!")
                sys.exit()

        screen.fill("black")

        for drawables in drawable:
            drawables.draw(screen)

        pygame.display.flip()
        dt = time_clock.tick(60) / 1000

        for shot in shots.copy():
            for asteroid in asteroids.copy():
                if shot.collision_check(asteroid):
                    shot.kill()
                    asteroid.kill()
                    break

if __name__ == "__main__":
    main()
