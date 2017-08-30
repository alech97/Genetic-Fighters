'''
Created on Aug 23, 2017
Handles a player in the hunger games.
@author: Alec Helyar
'''
from package.graphics import Circle, Point, Line
import package.sightline
import math
import package.special_math as spmath

class Player(object):
    '''
    This class handles a Player object
    '''
    #Add player health value
    def __init__(self, **vals):
        '''
        Constructor
        '''
        self.vals = vals
        self.vals['visuals'] = []
        self.vals['action'] = None
        self.vals['health'] = 100
        self.vals['weapon'] = None
        self.vals['reload_time'] = 0
        self.vals['laser_shots'] = []
        self.vals['bullets'] = []
        
        self.sightline = package.sightline.SightLine(
            vals['sightline_angle'], vals['point'], vals['angle'], 
            vals['win'], vals['color'], 
            vals['arenas'][0], vals['center'])
        
        self.c = Circle(vals['point'], vals['player_size'])
        self.c.setFill(vals['color'])
        self.c.setOutline(vals['color'])
        self.c.draw(self.vals['win'])
        print(vals['arenas'])
        
        
    def update(self, **input):
        for i in range(len(self.vals['bullets'])):
            dx, dy = self.vals['bullet_speed'] * math.cos(self.vals['bullets'][i][1]), self.vals['bullet_speed'] * math.sin(self.vals['bullets'][i][1])
            self.vals['bullets'][i][0].move(dx, dy)
            p2 = self.vals['bullets'][i][0].getP2()
            if p2.getX() < 0 or p2.getX() > 2 * self.vals['arenas'][0] or p2.getY() < 0 or p2.getY() > 2 * self.vals['arenas'][0]:
                self.vals['bullets'].remove(self.vals['bullets'][i])
                i -= 1
        for i in self.vals['laser_shots']:
            i[1] -= 1
            if i[1] == 0:
                i.undraw()
                self.vals['laser_shots'].remove(i)
        if self.vals['action']:
            self.vals['action'](self.vals['action_mag'])
        if self.vals['reload_time'] > 0:
            self.vals['reload_time'] -= 1
        if input:
            for key in input:
                self.vals[key] = input[key]
            self.make_decision()
        
    def make_decision(self):
        #TODO: implement
        pass
        
    def turn(self, angle):
        self.vals['angle'] += angle
        self.sightline.turn(angle)
        if self.vals['weapon']:
            self.vals['weapon'].turn(angle)
            
        
    def move(self, distance):
        point = self.vals['point'].getX(), self.vals['point'].getY()
        dx, dy = distance * math.cos(self.vals['angle']), distance * math.sin(self.vals['angle'])
        self.vals['point'] = Point(
            point[0] + dx, 
            point[1] + dy)
        self.c.move(dx, dy)
        self.sightline.move(self.vals['point'])
        if self.vals['weapon']:
            self.vals['weapon'].move(dx, dy)
        print(self.vals['point'], self.c, self.sightline.left)
        
    def fire(self, blank):
        if self.vals['weapon'] and self.vals['reload_time'] == 0:
            #Fire weapon!
            if type(self.vals['weapon']).__name__ == 'Gun':
                p1 = spmath.point_from_angle_distance(
                    self.vals['point'], self.vals['angle'], 
                    self.vals['bullet_start_dist'])
                p2 = spmath.point_from_angle_distance(
                    self.vals['point'], self.vals['angle'], 
                    self.vals['bullet_start_dist'] + self.vals['bullet_length'])
                bullet = Line(p1, p2)
                bullet.setWidth(self.vals['bullet_width'])
                bullet.setOutline('black')
                bullet.draw(self.vals['win'])
                self.vals['bullets'].append((bullet, self.vals['angle']))
                self.vals['reload_time'] = self.vals['gun_reload']
            else:
                p2 = spmath.point_from_angle_distance(
                    self.vals['point'], self.vals['angle'], 3000)
                laser = Line(self.vals['point'], p2)
                laser.setWidth(self.vals['laser_width'])
                laser.setOutline('red')
                laser.setFill('red')
                laser.draw(self.vals['win'])
                self.vals['laser_shots'].append(laser, self.vals['laser_health'])
        
        
        
        