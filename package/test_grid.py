'''
Created on Sep 2, 2017
This module tests the methods of grid.py
@author: Alec Helyar
'''
import unittest
from package.grid import Grid
from package.bullet import Bullet
from package.player import Player

class Test(unittest.TestCase):


    def setUp(self):
        self.grid = Grid(5)
        #Bullet in cells (0, 0) and (1, 0)
        self.b = Bullet(2, 2, 0, 1)
        #Player in cells (1,1) (2,1) (1, 2) and (2,2)
        self.p = Player(10, 10, 0, 0, 1)

    def test_add_and_rem_object(self):
        self.grid.add_object(self.b)
        self.assertEqual(len(self.grid.grid), 3)
        
        self.grid.add_object(self.p)
        self.assertEqual(len(self.grid.grid), 7)
        
        self.grid.remove_object(self.p)
        self.assertEqual(len(self.grid.grid), 3)
        
        self.grid.remove_object(self.b)
        self.assertEqual(len(self.grid.grid), 0)
        
    def test_check_collisions(self):
        self.grid.add_object(self.p)
        self.grid.add_object(self.b)
        p2 = Player(5, 5, 0, 0, 1)
        self.grid.add_object(p2)
        #(0,0) (1,0) (1,1) intersect
        
        collisions = self.grid.check_collisions()
        self.assertEqual(len(collisions), 0)
        
        #Player which intersects bullet and other player
        #TODO: Implement after adding player_test


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()