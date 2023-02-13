import pygame
from random import randint
import math


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
gas_particle_speed = [-5, 6]

oxygen_mass = 15.99903
hydrogen_mass = 2.0156
nitrogen_mass = 28.016


class Mouse:
    def __init__(self, size: int):
        self.size = size

    def create_circle(self, mouse_coord: tuple):
        circle = pygame.rect.Rect(mouse_coord[0] - self.size // 2, mouse_coord[1] - self.size // 2, self.size, self.size)
        return circle


class Particles:
    def __init__(self, surface, count: int, size: float, color: list, start_temp: int, mass: float, rand_size=False):
        self.surface = surface.get_size()
        self.surf = surface
        self.count = count
        self.color = color
        self.size = size
        self.temp = start_temp
        self.rand_size = rand_size
        self.particles = self.create_particles()    # [[x, y], [vx, vy], [ax, ay], size, color]
        self.mass = mass

    def create_particles(self):
        complete_particles = [
        [[randint(0, self.surface[0]), randint(0, self.surface[1])], [randint(gas_particle_speed[0], gas_particle_speed[1]), randint(gas_particle_speed[0], gas_particle_speed[1])], [0, 0], self.size, self.color]
        for _ in range(self.count)]
        return complete_particles

    def move(self):
        for particle in self.particles:
            vx = particle[1][0]
            vy = particle[1][1]

            particle[0][0] += vx
            particle[0][1] += vy

    def check_walls(self):
        for particle in self.particles:
            if particle[0][0] - particle[3] <= 0:
                particle[0][0] += 5
                particle[1][0] *= -1

            if particle[0][0] + particle[3] >= self.surface[0]:
                particle[0][0] -= 5
                particle[1][0] *= -1

            if particle[0][1] - particle[3] <= 0:
                particle[0][1] += 5
                particle[1][1] *= -1

            if particle[0][1] + particle[3] >= self.surface[1]:
                particle[0][1] -= 5
                particle[1][1] *= -1

    def distance(self, x1, y1, x2, y2):
        xDist = x2 - x1
        yDist = y2 - y1
        return math.sqrt(math.pow(xDist, 2) + math.pow(yDist, 2))

    def rotateVelocities(self, velocity, theta):
        rotatedVelocity = {
        "x": velocity[0] * math.cos(theta) - velocity[1] * math.sin(theta),     #[vx1] = [cos(theta) sin(theta)] [vx]
        "y": velocity[0] * math.sin(theta) + velocity[1] * math.cos(theta)      #[vy1] = -sin(theta) cos(theta)] [vy]
    }
        return rotatedVelocity

    def check_collision(self):
        for part in self.particles:
            for particle in self.particles:
                if part == particle:
                    continue
                if self.distance(part[0][0], part[0][1], particle[0][0], particle[0][1]) - part[3] * 2 < 0:
                    res = {"x": part[1][0] - particle[1][0], "y": part[1][1] - particle[1][1]}
                    if res["x"] * (particle[0][0] - part[0][0]) + res["y"] * (particle[0][1] - part[0][1]) >= 0:
                        theta = -math.atan2(particle[0][1] - part[0][1], particle[0][0] - part[0][0])

                        rotatedVelocity1 = self.rotateVelocities(part[1], theta)
                        rotatedVelocity2 = self.rotateVelocities(particle[1], theta)

                        swapVelocity1 = {"x": rotatedVelocity1["x"] * 0 / (self.mass + self.mass) + rotatedVelocity2["x"] * 2 * self.mass / (self.mass + self.mass), "y": rotatedVelocity1["y"]}
                        swapVelocity2 = {"x": rotatedVelocity2["x"] * 0 / (self.mass + self.mass) + rotatedVelocity1["x"] * 2 * self.mass / (self.mass + self.mass), "y": rotatedVelocity2["y"]}

                        u1 = self.rotateVelocities([swapVelocity1["x"], swapVelocity1["y"]], -theta)
                        u2 = self.rotateVelocities([swapVelocity2["x"], swapVelocity2["y"]], -theta)

                        part[1][0] = u1["x"]
                        part[1][1] = u1["y"]
                        particle[1][0] = u2["x"]
                        particle[1][1] = u2["y"]
                        particle[4] = [particle[1][0]**2+particle[1][1]**2 if particle[1][0]**2+particle[1][1]**2 <= 255 else 255, particle[4][1], particle[4][2]]

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(self.surf, particle[4], (particle[0][0], particle[0][1]), particle[3])


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
