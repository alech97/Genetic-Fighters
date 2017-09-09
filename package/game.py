'''
Created on Aug 29, 2017
Handles the game window and graphics
@author: Alec Helyar
'''
import sys, pygame, math, random
import package.special_math as spmath
from pygame import display, time
from package.grid import Grid
from package.bullet import bvals
from package.player import Player

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
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        vals['player_radius'])
    players.append(player)
    grid.add_object(player)

#Start simulation
while 1:
    #Check for closure
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
    
    #Clear Screen
    screen.fill((255, 255, 255))
    
    #Check Collisions
    collisions = grid.check_collisions()
    if collisions:
        for objcombo in collisions:
            for obj in objcombo:
                if type(obj).__name__ == 'Bullet' and obj in bullets:
                    bullets.remove(obj)
                    grid.remove_object(obj)
    grid.grid = []
    
    #Draw Arena
    pygame.draw.circle(
        screen, 0, 
        center, 
        vals['boundary'], 1)
    
    #Draw Players
    for player in players:
        return_value = player.make_turn('fire')
        if type(return_value).__name__ == 'Bullet':
            pygame.draw.circle(screen, player.color, player.get_point(), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            bullets.append(return_value)
            grid.add_object(return_value)
        if type(return_value).__name__ == 'Laser_shot':
            pygame.draw.circle(screen, player.color, player.get_point(), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            lasers.append(return_value)
            grid.add_object(return_value)
        elif type(return_value) is tuple:
            pygame.draw.circle(screen, player.color, return_value, vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
        else:
            pygame.draw.circle(screen, player.color, player.get_point(), vals['player_radius'], 0)
            pygame.draw.lines(screen, player.color, False, player.get_sightline_array(vals['sightline_angle']), 1)
            
        if player.weapon:
            pygame.draw.line(screen, player.weapon.color(), player.weapon.p1, player.weapon.p2, player.weapon.width())
        grid.add_object(player)
    
    #Draw Bullets
    for bullet in bullets:
        bullet.move()
        if not spmath.quick_in_range(center, bullet.get_p2(), vals['boundary']):
            bullets.remove(bullet)
            grid.remove_object(bullet)
        else:
            pygame.draw.line(screen, 0, bullet.get_p1(), bullet.get_p2(), bvals['bullet_width'])
            grid.add_object(bullet)
            
    #Draw Lasers
    for laser in lasers:
        if laser.decay():
            pygame.draw.line(screen, laser.color(), laser.get_p1(), laser.get_p2(), laser.width())
        else:
            lasers.remove(laser)
            grid.remove_object(laser)
    
    #Update display
    ms_elapsed = clock.tick(vals['fps'])
    display.flip()