'''
Created on Sep 1, 2017
Tests the bullet class and its methods
@author: Alec Helyar
'''
import unittest
from package.bullet import Bullet
from package.player import Player
import math


class Test(unittest.TestCase):


    def setUp(self):
        self.horiz1 = Bullet(4, 4, 0, 1)
        self.turned = Bullet(4, 4, math.pi / 2, 1)

    def test_const(self):
        self.assertEqual(self.horiz1.get_p1(), (4, 4))
        self.assertEqual(self.horiz1.get_p2(), (10, 4))
        self.assertEqual(self.turned.get_p1(), (4, 4))
        self.assertEqual(self.turned.get_p2(), (4, -2))
        
    def test_move(self):
        for i in range(10):
            self.horiz1.move()
            self.assertEqual(self.horiz1.get_p1(), (5 + i, 4))
            self.assertEqual(self.horiz1.get_p2(), (11 + i, 4))
            
    def test_turn(self):
        self.horiz1.turn(45 * math.pi / 180)
        self.assertLessEqual(abs(self.horiz1.p2[0] - 8.24264068712), .000001)
        self.assertAlmostEqual(self.horiz1.p2[1], -.24264068711)
        self.assertEqual(self.horiz1.get_p2(), (8, 0))
        
    def test_get_boundary(self):
        self.assertEqual(
            self.horiz1.get_bounding_points(), 
            (2, 12, 2, 6))
        
    def test_check_collision_bullet(self):
        horiz2 = Bullet(4, 10, 0, 1)
        self.assertFalse(self.horiz1.check_collision(horiz2))
        self.assertFalse(horiz2.check_collision(self.horiz1))

        horiz3 = Bullet(5, 4, 0, 1)
        self.assertTrue(self.horiz1.check_collision(horiz3))
        self.assertTrue(horiz3.check_collision(self.horiz1))
        
        vert1t = Bullet(6, 6, 1.57079, 1)
        self.assertTrue(self.horiz1.check_collision(vert1t))
        self.assertTrue(vert1t.check_collision(self.horiz1))
        
        vert2t = Bullet(4, 4, 1.57079, 1)
        self.assertTrue(self.horiz1.check_collision(vert2t))
        self.assertTrue(vert2t.check_collision(self.horiz1))
        
        vert3f = Bullet(3, 4, 1.57079, 1)
        self.assertFalse(self.horiz1.check_collision(vert3f))
        self.assertFalse(vert3f.check_collision(self.horiz1))
        
        vert4t = Bullet(10, 10, 1.5708, 1)
        self.assertTrue(self.horiz1.check_collision(vert4t))
        self.assertTrue(vert4t.check_collision(self.horiz1))
        
        horiz4 = Bullet(400, 4, 0, 1)
        self.assertFalse(self.horiz1.check_collision(horiz4))
        self.assertFalse(horiz4.check_collision(self.horiz1))
        
        vert5f = Bullet(10, 400, 1.5708, 1)
        self.assertFalse(vert4t.check_collision(vert5f))
        self.assertFalse(vert5f.check_collision(vert4t))
        
        
    def test_check_collision_player(self):
        ci1 = Player(7, 4, 0, 0, 1)
        ci2 = Player(11, 4, 0, 0, 1)
        ci3 = Player(7, 5, 0, 0, 1)
        cn1 = Player(4, 6, 0, 0, 1)
        cn2 = Player(4, 7, 0, 0, 2)
        
        self.assertTrue(self.horiz1.check_collision(ci1))
        self.assertTrue(self.horiz1.check_collision(ci2))
        self.assertTrue(self.horiz1.check_collision(ci3))
        self.assertFalse(self.horiz1.check_collision(cn1))
        self.assertFalse(self.horiz1.check_collision(cn2))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()