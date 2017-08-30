'''
Created on Aug 23, 2017
Handles a sightline object for each player
@author: Alec Helyar
'''
from package.graphics import Line, Point
import package.special_math as spmath
import math
    
class SightLine(object):
    """An object which dictates a player's sight"""
    
    def __init__(self, angle_diff, point, angle, win, color, arena, center):
        self.win = win
        self.color = color
        self.arena = arena
        self.left = None
        self.right = None
        self.center = center
        self.angle_diff = angle_diff
        self.point = point
        self.angle = angle
        self.sum_diff = 0
        self.update_lines()
        
    def move(self, point):
        self.point = point
        self.sum_diff += .1
        self.update_lines()
        
    def turn(self, angle):
        self.angle += angle
        self.sum_diff += abs(20 * angle)
        self.update_lines()
        
    def update_lines(self):
        if self.sum_diff > 2:
            self.sum_diff = 0
            left_points = self.point, spmath.point_from_angle_distance(
                self.point, self.angle + self.angle_diff, 40)
            right_points = self.point, spmath.point_from_angle_distance(
                self.point, self.angle - self.angle_diff, 40)
        
            #Check if intersects boundary
            #left_points = self.point, spmath.lineseg_intersects_circle(
            #    left_points[0], left_points[1], self.center, self.arena)
            #right_points = self.point, spmath.lineseg_intersects_circle(
            #    right_points[0], right_points[1], self.center, self.arena)
                
            #Update lines graphically
            if self.left:
                self.left.undraw()
                self.right.undraw()
            self.left = Line(left_points[0], left_points[1])
            self.right = Line(right_points[0], right_points[1])
            self.left.setFill(self.color)
            self.left.setWidth(.01)
            self.right.setWidth(.01)
            self.right.setFill(self.color)
            self.left.draw(self.win)
            self.right.draw(self.win)
    