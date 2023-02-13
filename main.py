import pygame
from mouse_circle import Mouse
from gas_particles import Particles


# CONST
WIDTH = 1100
HEIGHT = 700
FPS = 60

# COLORS
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BLUE = [1, 0, 128]
ROZA = [200, 0, 55]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [200, 200, 200]
YELLOW = [255, 255, 0]
COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (200, 0, 55), (255, 255, 255), (200, 200, 200), (255, 255, 0)]


# MAIN SETTINGS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heat gas")
clock = pygame.time.Clock()

# SIMULATION SETTINGS
mouse_circle_size = 50
mouse_circle_temp = 100
mouse_color = RED

gas_particle_size = 10
gas_particle_temp = 10
gas_particle_color = BLUE
gas_particle_count = 100
gas_particle_mass = 10

oxygen_mass = 15.99903
hydrogen_mass = 2.0156
nitrogen_mass = 28.016


def stop_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()


mouse = Mouse(mouse_circle_size)
gas_part = Particles(screen, gas_particle_count, gas_particle_size, gas_particle_color, gas_particle_temp, gas_particle_mass)


def main():
    circle = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_loop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    circle = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    circle = False

        screen.fill(BLACK)

        gas_part.draw_particles()
        gas_part.move()
        gas_part.check_walls()
        gas_part.check_collision()

        if circle:
            coord = pygame.mouse.get_pos()
            mouse_circle = mouse.create_circle(coord)
            #gas_part.check_collision_mouse(mouse_circle)
            pygame.draw.ellipse(screen, mouse_color, mouse_circle)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
