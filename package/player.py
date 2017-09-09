'''
Created on Sep 1, 2017
Handles a player object.
@author: Alec Helyar
'''
import package.special_math as spmath
import math

class Player():
    def __init__(self, x, y, angle, color, radius):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.weapon = None
        self.weapon_reload = 0
        self.health = 100
        self.radius = radius
        self.fitness = -1
        
    def get_point(self):
        return (int(self.x), int(self.y))
    
    def make_turn(self, action, mag=0):
        if self.health <= 0:
            return -1
        #IF FIRE IS CHOSEN, RETURNS BULLET, ELSE POINTS
        self.weapon_reload -= 1
        if action:
            return getattr(self, action)(mag)
    
    def get_sightline_array(self, angle_diff):
        point_list = []
        point_list.append(spmath.point_from_angle_distance(
            (self.x, self.y), self.angle - angle_diff, 20))
        point_list.append((self.x, self.y))
        point_list.append(spmath.point_from_angle_distance(
            (self.x, self.y), self.angle + angle_diff, 20))
        return point_list
    
    def move(self, dis):
        dx, dy = dis * math.cos(self.angle), dis * math.sin(self.angle)
        self.x, self.y = (
            self.x + dx, 
            self.y - dy)
        if self.weapon:
            self.weapon.move(dx, dy)
        
    def turn(self, angle):
        self.angle += angle
        self.angle = self.angle % (2 *  math.pi)
        if self.weapon:
            self.weapon.turn(angle)
        
    def fire(self, extra):
        if self.weapon and self.weapon_reload <= 0:
            self.weapon_reload = self.weapon.reload_ticks()
            return self.weapon.get_projectile(self)
        
    def damage(self, other):
        if type(other).__name__ == 'Bullet' or type(other).__name__ == 'Laser_shot':
            return other.damage(self)
        
    def check_collision(self, other):
        if self == other:
            return False
        elif type(other).__name__ == 'Laser_shot' and other.player != self:
            return spmath.width_lineseg_intersects_circle(
                other.width(), other.p1, other.p2, (self.x, self.y), self.radius)
        elif type(other).__name__ == 'Bullet' and other.player != self:
            return spmath.lineseg_intersects_circle(
                other.p1, other.p2, (self.x, self.y), self.radius)
        elif type(other).__name__ == 'Player':
            return spmath.dist_between_point(
                (self.x, self.y), (other.x , other.y)) <= 2 * self.radius
        return False
    
    def get_bounding_points(self):
        return (
            self.x - self.radius, 
            self.x + self.radius, 
            self.y - self.radius, 
            self.y + self.radius)
    