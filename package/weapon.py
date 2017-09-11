'''
Created on Sep 4, 2017
Handles the weapon object for a gun or laser.
@author: Alec Helyar
'''
import math 
from package.bullet import Bullet
from package.laser_shot import Laser_shot
import package.special_math as spmath

weapon_vals = {
    'laser': {
        'width':5,
        'length':20,
        'color':(255, 0, 0),
        'reload_turns':300
        },
   'gun': {
        'width':3,
        'length':10,
        'color':(0, 0, 0),
        'reload_turns':60
        }
    }

class Weapon():
    
    def __init__(self, x, y, angle, wtype='laser'):
        self.p1 = (x, y)
        self.angle = 0
        self.wtype = wtype
        self.turn(angle)
        
    def turn(self, angle):
        self.angle += angle
        self.angle = self.angle % (2 * math.pi)
        self.p2 = (
            self.p1[0] + math.cos(angle) * weapon_vals[self.wtype]['length'], 
            self.p1[1] - math.sin(angle) * weapon_vals[self.wtype]['length'])
        
    def move(self, dx, dy):
        self.p1 = (self.p1[0] + dx, self.p1[1] - dy)
        self.p2 = (self.p2[0] + dx, self.p2[1] - dy)
        
    def color(self):
        return weapon_vals[self.wtype]['color']
    
    def width(self):
        return weapon_vals[self.wtype]['width']
    
    def reload_ticks(self):
        return weapon_vals[self.wtype]['reload_turns']
    
    def get_projectile(self, player):
        if self.wtype == 'gun':
            point = spmath.point_from_angle_distance(self.p1, self.angle, weapon_vals[self.wtype]['length'])
            return Bullet(point[0], point[1], self.angle, .9, player)
        elif self.wtype == 'laser':
            point = spmath.point_from_angle_distance(self.p1, self.angle, weapon_vals[self.wtype]['length'])
            return Laser_shot(point[0], point[1], self.angle, player)
        
    def check_collision(self, other):
        #TODO: Check Collision
        pass
    
    def get_bounding_points(self):
        return (
            min(self.p1[0], self.p2[0]) - weapon_vals[self.wtype]['width'], 
            max(self.p1[0], self.p2[0]) + weapon_vals[self.wtype]['width'], 
            min(self.p1[1], self.p2[1]) - weapon_vals[self.wtype]['width'], 
            max(self.p1[1], self.p2[1]) + weapon_vals[self.wtype]['width'])