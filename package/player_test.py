'''
Created on Sep 2, 2017
Tests the player.py module.
@author: Alec Helyar
'''
import unittest
from package.player import Player
from package.bullet import Bullet
from math import pi
from package.special_math import dist_between_point
import package.weapon as weapon

class Test(unittest.TestCase):

    def setUp(self):
        self.p = Player(5.0, 5.0, 0, 0, 1)
        
    def test_get_point(self):
        self.assertEqual(self.p.get_point(), (5, 5))
        
    def test_turn(self):
        self.p.turn(pi)
        self.assertEqual(self.p.angle, pi)
        
        self.p.turn(- 6 * pi)
        self.assertEqual(self.p.angle, pi)
        
        self.p.turn(pi / 2)
        self.assertEqual(self.p.angle, pi * 3 / 2)
        
    def test_move(self):
        for i in range(10):
            self.assertEqual(
                (self.p.x, self.p.y), (5 + i, 5))
            self.p.move(1)
            
    def test_get_bounding_points(self):
        self.assertEqual(
            self.p.get_bounding_points(), (4, 6, 4, 6))
        
    def test_fire(self):
        self.assertIsNotNone(self.p.fire(666))
        self.assertEqual(self.p.weapon_reload, 666)
        self.assertIsNone(self.p.fire(666))
        
    def test_get_sightline_array(self):
        slist = self.p.get_sightline_array(pi / 9)
        self.assertEqual(len(slist), 3)
        self.assertAlmostEqual(dist_between_point(slist[0], slist[1]), 20)
        self.assertAlmostEqual(dist_between_point(slist[1], slist[2]), 20)
        
    def test_check_collision(self):
        pli = Player(6.0, 5.0, 0, 0, 1)
        pn = Player(8, 5, 0, 0, 1)
        bi = Bullet(5, 8, pi / 2, 1, self.p)
        bn = Bullet(5, 7, 0, 1, self.p)
        self.assertTrue(self.p.check_collision(pli))
        self.assertTrue(bi.check_collision(self.p))
        self.assertTrue(self.p.check_collision(bi))
        self.assertFalse(self.p.check_collision(pn))
        self.assertFalse(self.p.check_collision(bn))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()