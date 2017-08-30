'''
Created on Aug 26, 2017
Handles a laser weapon and its graphics
@author: Alec Helyar
'''
import package.graphics as graphics
import package.special_math as spmath
import math

class Laser():
    
    def __init__(self, player):
        self.angle = player.vals['angle']
        self.point = player.vals['point']
        self.width = player.vals['laser_width']
        self.height = player.vals['laser_height']
        self.win = player.vals['win']
        self.laser = graphics.Line(
            self.point, spmath.point_from_angle_distance(self.point, self.angle, self.height))
        self.laser.setWidth(self.width)
        self.laser.setOutline('red')
        self.laser.setFill('red')
        self.laser.draw(self.win)
        
    def move(self, d):
        self.laser.move(d * math.cos(self.angle), d * math.sin(self.angle))
        
    def turn(self, angle):
        if angle != 0:
            self.angle += angle
            self.laser.undraw()
            self.laser = graphics.Line(
                self.point, spmath.point_from_angle_distance(self.point, self.angle, self.height))
            self.laser.setWidth(self.width)
            self.laser.setOutline('red')
            self.laser.setFill('red')
            self.laser.draw(self.win)
            