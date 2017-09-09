'''
Created on Sep 1, 2017
Handles a bullet class.
@author: Alec Helyar
'''
import math
import package.special_math as spmath
bvals = {
    'bullet_length': 6,
    'bullet_width': 2,
    'damage': 30
    }

class Bullet():
    """Handles a bullet fired by a gun."""
    
    def __init__(self, x, y, angle, vel, player):
        self.p1 = (x, y)
        self.angle = 0
        self.turn(angle)
        self.vel = (vel * math.cos(angle), vel * math.sin(angle))
        self.player = player
        
    def get_p1(self):
        return (int(self.p1[0]), int(self.p1[1]))
    
    def get_p2(self):
        return (int(self.p2[0]), int(self.p2[1]))
    
    def move(self):
        self.p1 = self.p1[0] + self.vel[0], self.p1[1] + self.vel[1]
        self.p2 = self.p2[0] + self.vel[0], self.p2[1] + self.vel[1]
        return self.p1, self.p2
    
    def turn(self, angle_am):
        self.angle += angle_am
        self.p2 = (
            self.p1[0] + bvals['bullet_length'] * math.cos(self.angle), 
            self.p1[1] + bvals['bullet_length'] * math.sin(self.angle))
    
    def check_collision(self, other):
        if self == other:
            return False
        elif type(other).__name__ == 'Player' and other != self.player:
            return spmath.lineseg_intersects_circle(self.p1, self.p2, (other.x, other.y), other.radius)
        elif type(other).__name__ == 'Bullet':
            if spmath.linesegs_intersect(
                self.p1, self.p2, other.p1, other.p2):
                return True
        return False
            
    def get_bounding_points(self):
        return (
            min(self.p1[0], self.p2[0]) - bvals['bullet_width'], 
            max(self.p1[0], self.p2[0]) + bvals['bullet_width'], 
            min(self.p1[1], self.p2[1]) - bvals['bullet_width'], 
            max(self.p1[1], self.p2[1]) + bvals['bullet_width'])
    
    def damage(self, other):
        if type(other).__name__ == 'Player':
            other.health -= bvals['damage']
