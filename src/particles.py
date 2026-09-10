import math
import random

import pygame


class Particle:
    def __init__(self, x, y, color, velocity, life, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface):
        alpha = max(0, self.life / self.max_life)
        color = (*self.color[:3], int(255 * alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_explosion(self, x, y, color=(255, 180, 0), count=28):
        for _ in range(count):
            angle = random.uniform(0, 3.14159 * 2)
            speed = random.uniform(80, 260)
            self.particles.append(
                Particle(
                    x,
                    y,
                    color,
                    (math.cos(angle) * speed, math.sin(angle) * speed),
                    random.uniform(0.25, 0.8),
                    random.randint(2, 5),
                )
            )

    def add_hit(self, x, y, color=(255, 255, 255), count=12):
        for _ in range(count):
            angle = random.uniform(0, 3.14159 * 2)
            speed = random.uniform(30, 140)
            self.particles.append(
                Particle(
                    x,
                    y,
                    color,
                    (math.cos(angle) * speed, math.sin(angle) * speed),
                    random.uniform(0.18, 0.45),
                    random.randint(1, 3),
                )
            )

    def update(self, dt):
        for particle in list(self.particles):
            particle.update(dt)
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
