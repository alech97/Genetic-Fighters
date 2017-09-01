'''
Created on Aug 29, 2017
Handles the game window and graphics
@author: Alec Helyar
'''
import sys, pygame, math, random
import package.special_math as spmath
from pygame import display, time
import time as ptime
from package.grid import Grid
from package.bullet import Bullet, bvals

#Initialize python values
pygame.init()

#Options
vals = {
    'boundary':300,
    'margin':10,
    'info_panel_width':200,
    'player_radius':4,
    'num_players':12,
    'player_start_radius': 190,
    'sightline_angle': 30 * (math.pi / 180),
    'reload_turns': .5,
    'fps':120,
    'cell_size':20
    }

class Player():
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.weapon_reload = 0
        self.health = 100
        
    def get_point(self):
        return (int(self.x), int(self.y))
    
    def make_turn(self, action, mag):
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
        self.x, self.y = (
            self.x + dis * math.cos(self.angle), 
            self.y + dis * math.sin(self.angle))
        
    def turn(self, angle):
        self.angle += angle
        
    def fire(self, reload_ticks):
        if self.weapon_reload <= 0:
            self.weapon_reload = reload_ticks
            return Bullet(self.x, self.y, self.angle, .9)
        
    def check_collision(self, other):
        return False
    #TODO: Fix
    
    def get_bounding_points(self):
        return [
            (self.x - vals['player_radius'], self.y - vals['player_radius']), 
            (self.x - vals['player_radius'], self.y + vals['player_radius']), 
            (self.x + vals['player_radius'], self.y - vals['player_radius']), 
            (self.x + vals['player_radius'], self.y + vals['player_radius'])]
    


#Screen
screen = display.set_mode((
    vals['boundary'] * 2 + 2 * vals['margin'] + vals['info_panel_width'], 
    2 * vals['boundary'] + 2 * vals['margin']))

#Common variables
center = (vals['boundary'] + vals['margin'], 
          vals['boundary'] + vals['margin'])


#Initializations
clock = time.Clock()
players = []
bullets = []
lasers = []
ms_elapsed = 0
grid = Grid(20)

#Create players
angle = 2 * math.pi / vals['num_players']
for i in range(vals['num_players']):
    point = spmath.point_from_angle_distance(
        center, i * angle, vals['player_start_radius'])
    player = Player(
        point[0], point[1], i * angle + math.pi, 
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    players.append(player)
    grid.add_object(player)

#Start simulation
while 1:
    start = ptime.time()
    
    #Check for closure
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    closure = ptime.time() - start
    
    #Clear Screen
    screen.fill((255, 255, 255))
    
    #Check Collisions
    collisions = grid.check_collisions()
    if collisions:
        for obj in collisions:
            if type(obj[0]).__name__ == 'Bullet':
                if obj[0] in bullets:
                    bullets.remove(obj[0])
                grid.remove_object(obj[0])
            if type(obj[1]).__name__ == 'Bullet':
                if obj[1] in bullets:
                    bullets.remove(obj[1])
                grid.remove_object(obj[1])
    clear_screen = ptime.time() - closure
    
    #Draw Arena
    pygame.draw.circle(
        screen, 0, 
        center, 
        vals['boundary'], 1)
    draw_area = ptime.time() - clear_screen
    
    #Draw Players
    for player in players:
        #TODO: implement very efficient distance estimator to determine if out of bounds
        return_value = player.make_turn('fire', vals['fps'] * vals['reload_turns'])
        if type(return_value).__name__ == 'Bullet':
            pygame.draw.circle(screen, player.color, (player.x, player.y), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            bullets.append(return_value)
            grid.add_object(return_value)
        elif type(return_value) is tuple:
            pygame.draw.circle(screen, player.color, return_value, vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
        else:
            pygame.draw.circle(screen, player.color, (player.x, player.y), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
    
    draw_players = ptime.time() - draw_area
    
    #Draw Bullets
    for bullet in bullets:
        bullet.move()
        if not spmath.quick_in_range(center, bullet.get_p2(), vals['boundary']):
            bullets.remove(bullet)
        else:
            pygame.draw.line(screen, 0, bullet.get_p1(), bullet.get_p2(), bvals['bullet_width'])
    
    draw_bullets = ptime.time() - draw_players
    
    #Update display
    ms_elapsed = clock.tick(vals['fps'])
    display.flip()
    #print(clock.get_fps(), closure, clear_screen, draw_area, draw_players, draw_bullets, ptime.time() - draw_bullets)