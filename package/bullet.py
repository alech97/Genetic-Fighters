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
    }

class Bullet():
    """Handles a bullet fired by a gun."""
    
    def __init__(self, x, y, angle, vel):
        self.p1 = (x, y)
        self.p2 = (x + bvals['bullet_length'] * math.cos(angle), y + bvals['bullet_length'] * math.sin(angle))
        self.angle = angle
        self.vel = (vel * math.cos(angle), vel * math.sin(angle))
        
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
        if type(other).__name__ == 'Player':
            #TODO: Collision with player
            pass
        elif type(other).__name__ == 'Bullet':
            if spmath.linesegs_intersect(
                self.p1, self.p2, other.p1, other.p2):
                return True
        return False
            
    def get_bounding_points(self):
        u1 = (min(self.p1[0], self.p2[0]) - bvals['bullet_width'], min(self.p1[1], self.p2[1]) - bvals['bullet_width'])
        u2 = (max(self.p1[0], self.p2[0]) + bvals['bullet_width'], min(self.p1[1], self.p2[1]) - bvals['bullet_width'])
        u3 = (min(self.p1[0], self.p2[0]) - bvals['bullet_width'], max(self.p1[1], self.p2[1]) + bvals['bullet_width'])
        u4 = (max(self.p1[0], self.p2[0]) + bvals['bullet_width'], max(self.p1[1], self.p2[1]) + bvals['bullet_width'])
        return [u1, u2, u3, u4]
    
