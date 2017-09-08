'''
Created on Aug 23, 2017
This module contains math functions used by other modules.
@author: Alec Helyar
'''
import math

#Math Functions
def point_from_angle_distance(pos, angle_radians, distance):
    return (
        math.cos(angle_radians) * distance + pos[0], 
        math.sin(angle_radians) * distance + pos[1])
    
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

def dist_between_point(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow(p2[1] - p1[1], 2))

def vector_mag(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

def vector_projection(v1, v2):
    """Projects v2 onto v1"""
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    mag_squared = v1[0] * v1[0] + v1[1] * v1[1]
    if mag_squared != 0:
        return (v1[0] * dot / mag_squared, v1[1] * dot / mag_squared)
    return (0, 0)

def lineseg_intersects_circle(p1, p2, center, radius):
    ac = (center[0] - p1[0], center[1] - p1[1])
    p = vector_projection((p2[0] - p1[0], p2[1] - p1[1]), ac)
    return vector_mag((ac[0] - p[0], ac[1] - p[1])) <= radius
    
def linesegs_intersect(ap1, ap2, bp1, bp2):
    bottom = ((ap2[0] - ap1[0]) - (bp2[0] - bp1[0]), (ap2[1] - ap1[1]) - (bp2[1] - bp1[1]))
    #If not parallel (bottom == (0, 0))
    if bottom[0] != 0:
        t = ((bp1[0] - ap1[0]) / bottom[0] if bottom[0] != 0 else (bp1[0] - ap1[0]), (bp1[1] - ap1[1]) / bottom[1] if bottom[1] != 0 else (bp1[1] - ap1[1]))
        if 0 <= t[0] and t[0] <= 1:
            return True
    #Else if not colinear
    elif triangle_area(ap1, ap2, bp1) or triangle_area(ap2, bp1, bp2):
        return False
    #Else check if line seg's overlap
    else:
        top1 = (bp1[0] - ap1[0], bp1[1] - ap1[1])
        top2 = (bp2[0] - ap1[0], bp2[1] - ap1[1])
        va = (ap2[0] - ap1[0], ap2[1] - ap1[1])
        t1 = (top1[0] / va[0] if va[0] != 0 else top1[0], top1[1] / va[1] if va[1] != 0 else top1[1])
        t2 = (top2[0] / va[0] if va[0] != 0 else top2[0], top2[1] / va[1] if va[1] != 0 else top2[1])
        return (0 <= t1[0] and t1[0] <= 1) or (0 <= t2[0] and t2[0] <= 1)
    return False
    
def triangle_area(p1, p2, p3):
    return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2)
    
def enemy_in_sight(angle1, angle2, angle_diff):
    angle1, angle2 = angle1 % (2 * math.pi), angle2 % (2 * math.pi)
    diff = math.pi - abs(abs(angle2 - angle1) - math.pi)
    return abs(diff) <= angle_diff