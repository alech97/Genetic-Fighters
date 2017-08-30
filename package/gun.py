'''
Created on Aug 26, 2017
Handles a gun and its graphics
@author: Alec Helyar
'''
import package.graphics as graphics
import package.special_math as spmath
import math

class Gun():
    
    def __init__(self, player):
        self.angle = player.vals['angle']
        self.point = player.vals['point']
        self.width = player.vals['gun_width']
        self.height = player.vals['gun_height']
        self.win = player.vals['win']
        self.gun = graphics.Line(
            self.point, spmath.point_from_angle_distance(self.point, self.angle, self.height))
        self.gun.setWidth(self.width)
        self.gun.setOutline('black')
        self.gun.setFill('black')
        self.gun.draw(self.win)
        
        self.angle_sum = 0
        
    def move(self, dx, dy):
        self.gun.move(dx, dy)
        self.point.move(dx, dy)
        
    def turn(self, angle):
        if angle != 0:
            self.angle += angle
            self.angle_sum += angle
            if abs(self.angle_sum) > .1:
                self.angle_sum = 0
                self.gun.undraw()
                self.gun = graphics.Line(
                    self.point, spmath.point_from_angle_distance(self.point, self.angle, self.height))
                self.gun.setWidth(self.width)
                self.gun.setOutline('black')
                self.gun.setFill('black')
                self.gun.draw(self.win)
            