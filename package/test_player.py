'''
Created on Aug 25, 2017
This class tests the player class
@author: Alec Helyar
'''
import package.player as player
import package.graphics as graphics
import math
import package.gun as gun
import time
from time import sleep

def update(vals, player1, turn):
    if turn:
        player1.update(visuals=None)
    else:
        player1.update()

def main():
    win = graphics.GraphWin("Test", 600, 600)
    vals = {'angle':-1 * math.pi / 2, 'sightline_angle':math.pi/4, 'gun_reload':300, 'turn_length':.001,
            'win':win, 'player_size':5, 'bullet_start_dist':3, 'bullet_length':4,'bullet_width':3, 'bullet_speed':.25,
            'turn_angle':math.pi/10, 'arenas':[300], 'point':player.Point(300, 300), 'gun_width':3, 'gun_height':9, 'laser_width':3, 'laser_height':5}
    player1 = player.Player(sightline_angle=vals['sightline_angle'],angle=vals['angle'], win=vals['win'],
                            player_size=vals['player_size'],turn_angle=vals['turn_angle'],
                            arenas=vals['arenas'], point=vals['point'], color='orange', gun_reload=vals['gun_reload'], gun_height=vals['gun_height'],
                            center=vals['point'], bullet_start_dist=vals['bullet_start_dist'], laser_width=vals['laser_width'], laser_height=vals['laser_height'],
                            bullet_length=vals['bullet_length'], bullet_width=vals['bullet_width'], bullet_speed=vals['bullet_speed'], gun_width=vals['gun_width'])
    graphics.Circle(vals['point'], vals['arenas'][0]).draw(vals['win'])
    player1.vals['action'] = player1.turn
    player1.vals['action_mag'] = .01
    player1.vals['weapon'] = gun.Gun(player1)
    
    while 1:
        start = time.clock()
        if win.checkMouse():
            win.close()
            break
        a = win.checkKey()
        if a != "":
            print(a)
            if a == 'a':
                player1.vals['action'] = player1.turn
                player1.vals['action_mag'] = -.01
            elif a == 'd':
                player1.vals['action'] = player1.turn
                player1.vals['action_mag'] = .01
            elif a == 'w':
                player1.vals['action'] = player1.move
                player1.vals['action_mag'] = .2
            elif a == 's':
                player1.vals['action'] = player1.fire
                player1.vals['action_mag'] = .2
        update(vals, player1, turn=True)
        elapsed = time.clock() - start
        time.sleep(vals['turn_length'] - elapsed if vals['turn_length'] > elapsed else 0)
        
main()

if __name__ == '__main__':
    pass