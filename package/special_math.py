'''
Created on Aug 23, 2017
This module contains math functions used by other modules.
@author: Alec Helyar
'''
import math
from package.graphics import Point

#Math Functions
def point_from_angle_distance(pos, angle_radians, distance):
    return (
        round(math.cos(angle_radians) * distance + pos[0]), 
        round(math.sin(angle_radians) * distance + pos[1]))
    
def quick_in_range(center, point, dis):
    if point[0] >= center[0] - dis and point[0] <= center[0] + dis and \
        point[1] >= center[1] - dis and point[1] <= center[1] + dis:
        return dist_between_point(center, point) <= dis
    return False
    
    
def cross_product(self, point1, point2):
    return point1.getX() * point2.getY() - point1.getY() * point2.getX()

def angle_from_pos_to_point(pos, point):
    return math.atan2(
        point.getY() - pos.getY(), point.getX() - pos.getX())
    
def line_from_lineseg(p1, p2):
    return (p1.getY() - p2.getY(), 
            p2.getX() - p1.getX(), 
            -1*(p1.getX() * p2.getY() - p2.getX() * p1.getY()))

def dist_between_point(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow(p2[1] - p1[1], 2))
    
#TODO: Find better version of this that doesnt binary search
def lineseg_intersects_circle(p1, p2, center, radius):
    #binary search for intersection, p1 must be player since t lower interval
    # is 0
    
    #plug in t value and returns radius from center
    def distance_between_point_and_t(t):
        point = (
            p1.getX() + t * (p2.getX() - p1.getX()), 
            p1.getY() + t * (p2.getY() - p1.getY()))
        return math.sqrt(math.pow((point[0] - center.getX()), 2) + math.pow(point[1] - center.getY(), 2))

    def binary_search(lower, upper):
        middle = (upper + lower) / 2
        check = distance_between_point_and_t(middle)
        if abs(radius - check) <= 0.1:
            return Point(
                p1.getX() + middle * (p2.getX() - p1.getX()), 
                p1.getY() + middle * (p2.getY() - p1.getY()))
        elif radius > check:
            return binary_search(middle, upper)
        else:
            return binary_search(lower, middle)
        
    return binary_search(0, 1)
    
def linesegs_intersect(ap1, ap2, bp1, bp2):
    L1 = line_from_lineseg(ap1, ap2)
    L2 = line_from_lineseg(bp1, bp2)
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if x >= min(ap1.getX(), ap2.getX()) and \
        x <= max(ap1.getX(), ap2.getX()) and \
        y >= min(ap1.getY(), ap2.getY()) and \
        y <= max(ap1.getY(), ap2.getY()):
            return x,y
    else:
        return None
    
def enemy_in_sight(angle1, angle2, angle_diff):
    angle1, angle2 = angle1 % (2 * math.pi), angle2 % (2 * math.pi)
    diff = math.pi - abs(abs(angle2 - angle1) - math.pi)
    return abs(diff) <= angle_diff