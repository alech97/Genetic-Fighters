'''
Created on Aug 23, 2017
Launches a hunger games window.
@author: Alec Helyar
'''
from package.graphics import Line, Point, GraphWin, GraphicsError, Circle
from time import sleep
from package.player import Player
import random
import package.special_math as spmath
from math import pi


class HungerGame:
    """A HungerGame simulation"""
    #TODO: Add guns and lasers to start, change player color to attribute of gene, add projectile list and method which iterates through collisions,
    #TODO: Add "brain" input class
    #TODO: Change update to only sleep for uncomputed time
    
    def __init__(self):
        #Initial Options
        self.players = []
        self.weapons = []
        self.colors = ['black', 'blue', 'red', 
                  'orange', 'magenta', 'brown', 
                  'pink', 'purple', 'green', 'yellow']
        self.options = {'num_players':10, 'background':'white', 
                        'title':'My Genes', 'game_radius':400,
                        'player_start_radius': 300, 'player_size':3, 
                        'turn_length': 1,'update_unit':100,
                        'sightline_angle_deg':45, 'shrink_factor':.20, 
                        'margin':10, 'info_panel_width':200, 'num_shrinks':3,
                        'turns_per_shrink':10, 'num_hidden_layers':1, 
                        'num_guns':3, 'num_lasers':3, 'gun_dist':30, 
                        'laser_dist': 10, 'gun_size':5, 'laser_size':7, 
                        'gun_width':3, 'laser_width':3, 'arena_damage':20,
                        'turn_angle_deg':10}
        
        #Initialize game variables
        self.win = GraphWin(
            self.options['title'], 
            self.options['game_radius'] * 2 + 2 * self.options['margin'] + \
            self.options['info_panel_width'], 
            self.options['game_radius'] * 2 + 2 * self.options['margin'])
        self.win.setBackground(self.options['background'])
        self.sightline_angle = self.options['sightline_angle_deg'] * pi / 360
        self.turn_progress = self.options['update_unit'] - 1
        self.center = Point(
            self.options['margin'] + self.options['game_radius'], 
            self.options['margin'] + self.options['game_radius'])
        self.arena_index = 0
        self.arena_progress = 0
        
        #Game Boundaries
        self.arenas = []
        for i in range(self.options['num_shrinks']):
            self.arenas.append(
                self.options['game_radius'] - (
                    i * self.options['shrink_factor'] * self.options['game_radius']))
        self.boundary = Circle(self.center, self.arenas[0])
        self.boundary.draw(self.win)
        self.arena = Circle(self.center, self.arenas[self.arena_index])
        self.arena.draw(self.win)
        
        #Launch game
        self.create_players()
        self.create_weapons()
        self.main()
        
        
    def update(self):
        """Updates the game for every player"""
        sleep(self.options['turn_length'] / self.options['update_unit'])
        for player in self.players:
            if self.turn_progress + 1 == self.options['update_unit']:
                self.give_player_visual(player)
                player.make_decision()
            #if spmath.dist_between_point(
            #  self.center, player.vals['point']) > self.arenas[self.arena_index]:
                #player.vals['health'] -= self.options['arena_damage']
                
            player.update()
        self.turn_progress += 1
        if self.turn_progress == self.options['update_unit']:
            self.turn_progress = 1
            self.arena_progress += 1
        if self.arena_progress == self.options['turns_per_shrink'] and self.arena_index + 1 != len(self.arenas):
            self.arena_progress = 0
            self.arena_index += 1
            self.arena.undraw()
            self.arena = Circle(self.center, self.arenas[self.arena_index])
            self.arena.draw(self.win)
            self.arena.setOutline('blue')
            
    def give_player_visual(self, player):
        angle, point = player.vals['angle'], player.vals['point']
        player.visuals = []
        for enemy in self.players:
            if enemy == player:
                continue
            enemy_angle = spmath.angle_from_pos_to_point(
                point, enemy.vals['point'])
            if spmath.enemy_in_sight(angle, enemy_angle, self.sightline_angle):
                player.visuals.append(enemy)
                
    def create_weapons(self):
        #TODO: Create weapons
        weapon_num = self.options['num_guns'] + self.options['num_lasers']
        angles = list(range(weapon_num))
        angle_step = 2 * pi / weapon_num
        rand_factor = random.uniform(-1 * angle_step, angle_step)
        for q in angles:
            angles[q] = angles[q] * (angle_step) + rand_factor
        random.shuffle(angles)
        
        print(angles, rand_factor, weapon_num, angle_step)
        for i in range(self.options['num_guns']):
            # Place gun at angles[i]
            new_gun = Line(
                spmath.point_from_angle_distance(self.center, angles[i], self.options['gun_dist']), 
                spmath.point_from_angle_distance(self.center, angles[i], self.options['gun_dist'] + self.options['gun_size']))
            new_gun.setOutline('black')
            new_gun.setWidth(self.options['gun_width'])
            new_gun.draw(self.win)
            self.weapons.append(new_gun)
            
        for x in range(self.options['num_lasers']):
            # Place laser at angles[i + x]
            new_laser = Line(
                spmath.point_from_angle_distance(self.center, angles[x + i], self.options['laser_dist']), 
                spmath.point_from_angle_distance(self.center, angles[x + i], self.options['laser_dist'] + self.options['laser_size']))
            new_laser.setOutline('red')
            new_laser.setWidth(self.options['laser_width'])
            new_laser.draw(self.win)
            self.weapons.append(new_laser)
            
        print(len(self.weapons))

    def main(self):
        while 1:
            self.update()
            try:
                if self.win.checkMouse():
                    break
            except GraphicsError:
                pass
            
        try:
            self.win.close()    # Close window when done
        except GraphicsError:
            pass
        return
        
    def create_players(self):
        angle = 2 * pi / self.options['num_players']
        rand_colors = random.sample(self.colors, len(self.colors))
        for i in range(self.options['num_players']):
            player = Player(
                angle=i * angle + pi,
                sightline_angle=self.sightline_angle,
                update_unit=self.options["update_unit"], 
                win=self.win, color=rand_colors[i % len(rand_colors)], 
                player_size=self.options['player_size'], 
                turn_angle=self.options['turn_angle_deg'] * pi / 180,
                arenas=self.arenas, center=self.center,
                point=spmath.point_from_angle_distance(
                    self.center, i * angle, self.options['player_start_radius']))
            self.players.append(player)
    
if __name__ == '__main__':
    HungerGame()