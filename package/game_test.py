'''
Created on Aug 29, 2017
Tests the game window and graphics
@author: Alec Helyar
'''
import sys, pygame, math
import package.special_math as spmath
from pygame import display, time
from package.grid import Grid
from package.bullet import bvals
from package.player import Player
from package.weapon import Weapon

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

#TEST VARIABLES
p1 = Player(150, 310, 0, (234,56,63), vals['player_radius'])
players.append(p1)
grid.add_object(p1)
p1.weapon = Weapon(p1.x, p1.y, p1.angle)
p2 = Player(480, 310, math.pi, (234,56,63), vals['player_radius'])
players.append(p2)
grid.add_object(p2)
p2.weapon = Weapon(p2.x, p2.y, p2.angle, 'gun')


#Start simulation
while 1:
    #Check for closure
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
            
    #TESTING
    print([player.health for player in players])
    
    #Clear Screen
    screen.fill((255, 255, 255))
    
    #Check Collisions
    collisions = grid.check_collisions()
    if collisions:
        for objcombo in collisions:
            objcombo[0].damage(objcombo[1])
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
        elif return_value == -1:
            #Player is dead
            players.remove(player)
            continue
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