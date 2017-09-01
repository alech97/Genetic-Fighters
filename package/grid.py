'''
Created on Sep 1, 2017
Handles a grid class which is used to detect collisions.
@author: Alec Helyar
'''
from itertools import combinations

class Grid():
    """Grid class handles collisions"""
    
    def __init__(self, cell_size):
        """
        Create grid
        :param cell_size: The size of each cell in the grid
        """
        self.cell_size = cell_size
        self.grid = []
        #TODO: Implement grid
        
    def add_object(self, obj):
        bounds = obj.get_bounding_points()
        bounds = set([((b[0] - (b[0] % self.cell_size)) / self.cell_size, (b[1] - (b[1] % self.cell_size)) / self.cell_size) for b in bounds])
        for b in bounds:
            self.grid.append((b, obj))
        
    def remove_object(self, rem_object):
        for obj in self.grid:
            if obj[1] == rem_object:
                self.grid.remove(obj)
                
    def check_collisions(self):
        #Objects in collisions
        collisions = []
        self.grid = sorted(self.grid, key=lambda tup: tup[0])
        def check_list(olist):
            for a, b in combinations(olist, 2):
                if a[1].check_collision(b[1]):
                    collisions.append((a[1], b[1]))
                
        start_index = 0
        end_index = 1
        for i in range(1, len(self.grid)):
            if self.grid[i][0] != self.grid[start_index][0]:
                if end_index - start_index > 1:
                    check_list(self.grid[start_index:end_index])
                start_index, end_index = i, i + 1
            else:
                end_index += 1
        return collisions