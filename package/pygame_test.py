'''
Created on Aug 29, 2017
Handles the game window and graphics
@author: Alec Helyar
'''
import sys, pygame, math, random
import package.special_math as spmath
from pygame import display, time
pygame.init()

class Player():
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.vel = 10 #In pixels per second
        
    def get_point(self):
        return (int(self.x), int(self.y))
    
    def update(self, ms_elapsed):
        vel = self.vel * ms_elapsed / 1000
        self.x, self.y = (
            self.x + vel * math.cos(self.angle), 
            self.y + vel * math.sin(self.angle))
        return self.get_point()
    
    def get_sightline_array(self, angle_diff):
        point_list = []
        point_list.append(spmath.point_from_angle_distance(
            (self.x, self.y), self.angle - angle_diff, 20))
        point_list.append((self.x, self.y))
        point_list.append(spmath.point_from_angle_distance(
            (self.x, self.y), self.angle + angle_diff, 20))
        return point_list

#Options
vals = {
    'boundary':300,
    'margin':10,
    'info_panel_width':200,
    'player_radius':4,
    'num_players':12,
    'player_start_radius': 190,
    'sightline_angle': 30 * (math.pi / 180)
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
        pygame.draw.circle(screen, player.color, player.update(ms_elapsed), vals['player_radius'], 0)
        pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
    
    #Update display
    ms_elapsed = clock.tick(120)
    print(ms_elapsed)
    display.flip()