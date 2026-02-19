import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    SIZE_MAP = {
        ASTEROID_MIN_RADIUS: ("small", 10, "#f5f056"),  # Yellow
        ASTEROID_MIN_RADIUS * 2: ("medium", 15, "#ff3838"),  # Red
        ASTEROID_MIN_RADIUS * ASTEROID_KINDS: ("large", 20, "#47b3ff")  # Blue
    }

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.size, self.points, self.color =  self.SIZE_MAP.get(
            radius, ("unknown", 0, "#FFFFFF")
        )

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def check_collision(self, circleshape_obj):
        return super().check_collision(circleshape_obj)
    
    def getPoints(self):
        return self.points
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)

        v1 = self.velocity.rotate(random_angle)
        v2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        obj1 = Asteroid(self.position.x, self.position.y, new_radius)
        obj2 = Asteroid(self.position.x, self.position.y, new_radius)

        obj1.velocity = v1 * 1.2
        obj2.velocity = v2 * 1.2

    