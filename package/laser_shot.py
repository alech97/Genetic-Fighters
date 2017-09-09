'''
Created on Sep 9, 2017
Handles a laser shot class.
@author: Alec Helyar
'''
import math
import package.special_math as spmath
lvals = {
    'laser_length': 2000,
    'laser_width': 1,
    'health':10,
    'decay_vel':2,
    'decay_accel':-0.2,
    'damage': 25
    }

class Laser_shot():
    """Handles a bullet fired by a gun."""
    
    def __init__(self, x, y, angle, player):
        self.p1 = (x, y)
        self.angle = 0
        self.turn(angle)
        self.player = player
        self.health = lvals['health']
        self.decay_vel = lvals['decay_vel']
        
    def decay(self):
        self.health += self.decay_vel
        self.decay_vel += lvals['decay_accel']
        return self.health >= 0
    
    def color(self):
        return (255, 0, 0)
    
    def width(self):
        return int(lvals['laser_width'] * self.health)
        
    def get_p1(self):
        return (int(self.p1[0]), int(self.p1[1]))
    
    def get_p2(self):
        return (int(self.p2[0]), int(self.p2[1]))
    
    def turn(self, angle_am):
        self.angle += angle_am
        self.p2 = (
            self.p1[0] + lvals['laser_length'] * math.cos(self.angle), 
            self.p1[1] + lvals['laser_length'] * math.sin(self.angle))
        
    def damage(self, other):
        if type(other).__name__ == "Player":
            other.health -= lvals['damage']
    
    def check_collision(self, other):
        if self == other:
            return False
        elif type(other).__name__ == 'Player' and other != self.player:
            return spmath.width_lineseg_intersects_circle(
                self.width(), self.p1, self.p2, (other.x, other.y), other.radius)
        return False
            
    def get_bounding_points(self):
        return (
            min(self.p1[0], self.p2[0]) - lvals['laser_width'], 
            max(self.p1[0], self.p2[0]) + lvals['laser_width'], 
            min(self.p1[1], self.p2[1]) - lvals['laser_width'], 
            max(self.p1[1], self.p2[1]) + lvals['laser_width'])