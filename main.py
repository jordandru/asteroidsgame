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

    high_score = 0

    try:
        with open("highscore.txt", "r") as file_object:
            content = file_object.read()
            if content.strip():
                high_score = int(content.strip())
            else:
                high_score = 0
    except FileNotFoundError:
        high_score = 0
    except ValueError:
        print("Warning: highscore.txt contains invalid data. Resetting high score to 0.")
        high_score = 0


    time_clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    my_font = pygame.font.SysFont("Marker", 30)

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
                print(f"Final Score: {my_player.score}")
                if my_player.score > high_score:
                    high_score = my_player.score
                    with open("highscore.txt", "w") as file_object:
                        file_object.write(str(high_score))

                print(f"High Score: {high_score}")
                sys.exit()

        screen.fill("black")

        text_surface = my_font.render(f"Score: {my_player.score}", True, (0, 0, 255))
        screen.blit(text_surface, (10, 10))

        for drawables in drawable:
            drawables.draw(screen)

        pygame.display.flip()
        dt = time_clock.tick(60) / 1000

        for shot in shots.copy():
            for asteroid in asteroids.copy():
                if shot.collision_check(asteroid):
                    shot.kill()
                    asteroid.split()
                    my_player.score += PLAYER_POINTS_FOR_HIT
                    break

if __name__ == "__main__":
    main()
