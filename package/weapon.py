'''
Created on Sep 4, 2017
Hanldes the weapon object for a gun or laser.
@author: Alec Helyar
'''
import math 

weapon_vals = {
    'laser': {
        'width':2,
        'length':5,
        'color':(255, 0, 0)
        },
   'gun': {
        'width':1,
        'length':3,
        'color':(0, 0, 0)
        }
    }

class Weapon():
    
    def __init__(self, wtype='laser', x, y, angle):
        self.p1 = (x, y)
        self.angle = 0
        self.wtype = wtype
        self.turn(angle)
        
    def turn(self, angle):
        self.angle += angle
        self.angle = self.angle % (2 * math.pi)
        self.p2 = (
            self.x + math.cos(angle) * weapon_vals[self.wtype]['length'], 
            self.y - math.sin(angle) * weapon_vals[self.wtype]['length'])
        
    def move(self, dx, dy):
        self.p1 = (self.p1[0] + dx, self.p1[1] - dy)
        self.p2 = (self.p2[0] + dx, self.p2[1] - dy)