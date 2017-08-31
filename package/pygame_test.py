'''
Created on Aug 29, 2017
Handles the game window and graphics
@author: Alec Helyar
'''
import sys, pygame, math, random
import package.special_math as spmath
from pygame import display, time
pygame.init()

class Grid():
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = []
        #TODO: Implement grid
        
    def add_bullet(self, bullet):
        cell_one = ((bullet.p1[0] - (bullet.p1[0] % self.cell_size)) / self.width, (bullet.p1[1] - (bullet.p1[1] % self.cell_size)) / self.height)
        cell_two = ((bullet.p2[0] - (bullet.p2[0] % self.cell_size)) / self.width, (bullet.p2[1] - (bullet.p2[1] % self.cell_size)) / self.height)
        if (cell_one, bullet) not in self.grid:
            self.grid.append((cell_one, bullet))
        if cell_one != cell_two and (cell_two, bullet) not in self.grid:
            self.grid.append((cell_two, bullet))
    
    def add_player(self, player):
        cell_one = (player.x - (player.x % self.cell_size)) / self.width, (player.y - (player.y % self.cell_size)) / self.height
        if (cell_one, player) not in self.grid:
            self.grid.append((cell_one, player))
        
    def remove_object(self, rem_object):
        for obj in self.grid:
            if obj[1] == rem_object:
                self.grid.remove(obj)
                
    def check_collisions(self):
        self.grid = sorted(self.grid, key=lambda tup: tup[0])
        
        for i in range(len(self.objects)):
            

class Bullet():
    def __init__(self, x, y, angle, vel, length):
        self.p1 = (x, y)
        self.p2 = (x + length * math.cos(angle), y + length * math.sin(angle))
        self.angle = angle
        self.vel = (vel * math.cos(angle), vel * math.sin(angle))
        
    def get_p1(self):
        return (int(self.p1[0]), int(self.p1[1]))
    
    def get_p2(self):
        return (int(self.p2[0]), int(self.p2[1]))
    
    def move(self):
        self.p1 = self.p1[0] + self.vel[0], self.p1[1] + self.vel[1]
        self.p2 = self.p2[0] + self.vel[0], self.p2[1] + self.vel[1]
        return self.p1, self.p2
        

class Player():
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.weapon_reload = 0
        
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
            return Bullet(self.x, self.y, self.angle, .9, 5)
        
def check_bullet_overlap(bullet_list):
    #Create a sorted list of bullets of the form: (p1, p2, bullet) sorted by x value of p1
    range_list = sorted([(bullet.get_p1(), bullet.get_p2(), bullet) for bullet in bullet_list], key=lambda tup: tup[0][0])
    

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
    'bullet_length': 4,
    'bullet_width': 2,
    'cell_size':20
    }

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

#Create players
angle = 2 * math.pi / vals['num_players']
for i in range(vals['num_players']):
    point = spmath.point_from_angle_distance(
        center, i * angle, vals['player_start_radius'])
    player = Player(
        point[0], point[1], i * angle + math.pi, 
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    players.append(player)

#Start simulation
while 1:
    #Check for closure
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    
    #Clear Screen
    screen.fill((255, 255, 255))
    
    #Draw Arena
    pygame.draw.circle(
        screen, 0, 
        center, 
        vals['boundary'], 1)
    
    #Draw Players
    for player in players:
        #TODO: implement very efficient distance estimator to determine if out of bounds
        return_value = player.make_turn('fire', vals['fps'] * vals['reload_turns'])
        if type(return_value).__name__ == 'Bullet':
            pygame.draw.circle(screen, player.color, (player.x, player.y), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            bullets.append(return_value)
        elif type(return_value) is tuple:
            pygame.draw.circle(screen, player.color, return_value, vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
        else:
            pygame.draw.circle(screen, player.color, (player.x, player.y), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            
    #Draw Bullets
    for bullet in bullets:
        check_bullet_overlap(bullets)
        bullet.move()
        if not spmath.quick_in_range(center, bullet.get_p2(), vals['boundary']):
            bullets.remove(bullet)
        else:
            pygame.draw.line(screen, 0, bullet.get_p1(), bullet.get_p2(), vals['bullet_width'])
    
    #Update display
    ms_elapsed = clock.tick(vals['fps'])
    display.flip()