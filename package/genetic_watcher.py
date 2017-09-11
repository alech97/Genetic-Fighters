'''
Created on Sep 9, 2017
This class handles the genetic code of the game.
It is essentially god of the simulation.
@author: Alec Helyar
'''
import random

class Mastermind():

    def __init__(self, num_players=12):
        '''
        Constructor
        '''
        self.num_players = num_players
        self.num_set_of_parents = int(num_players / 8)
        self.num_chromosomes = 48
        
        #List of (player_index, player_color, player, genes)
        self.population = []
        
    #TODO: Initialize Population
    
    def create_player(self, genes=None):
        #TODO: Create player with custom color, index, and genes
        pass
    
    #TODO: Method to sort population by fitness
    
    #TODO: New Generation- Determine parents and nonsurvivors and generate and introduce offspring
    def new_generation(self):
        #Roulette wheel parent selection---------------------------------------
        fitness_sum = 0
        for genum in self.population:
            fitness_sum += genum[2].fitness
        
        #Choose parents
        chosen_parents = []
        parents = []
        while len(parents) < self.num_set_of_parents:
            parent_one = self.roulette_parent_selection(fitness_sum)
            parent_two = self.roulette_parent_selection(fitness_sum)
            if parent_one != parent_two and \
            parent_one not in chosen_parents and \
            parent_two not in chosen_parents:
                chosen_parents.append(parent_one)
                chosen_parents.append(parent_two)
                parents.append((parent_one, parent_two))
        
        #TODO: Generate offpsring--------------------------
        #Biased one-point crossover
        offspring = []
        for p in parents:
            offspring += self.crossover_genes(p)
        
        #TODO: Random-resetting mutation
        #--------------------------------------------------
        
        #TODO: Remove nonsurvivors and add offspring
        
        #End with new generation
        
    def crossover_genes(self, parents):
        point = int(round(
            (parents[0][2].fitness * self.num_chromosomes) / (
                parents[0][2].fitness + parents[1][2].fitness)))
        c1_genes = parents[0][3][0:point] + parents[1][3][point:]
        c2_genes = parents[1][3][0:point] + parents[0][3][point:]
        return [self.create_player(c1_genes), self.create_player(c2_genes)]
        
    def roulette_parent_selection(self, ssum):
        chosen_p = random.randint(0, ssum)
        p = 0
        for g in self.population:
            p += g[2].fitness
            if p >= chosen_p:
                return g
            
    #TODO: Run game and find fitness values