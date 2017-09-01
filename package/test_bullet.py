'''
Created on Sep 1, 2017
Tests the bullet class and its methods
@author: Alec Helyar
'''
import unittest
from package.bullet import Bullet


class Test(unittest.TestCase):


    def setUp(self):
        self.horiz1 = Bullet(4, 4, 0, 1)

    def test_const(self):
        self.assertEqual(self.horiz1.get_p1(), (4, 4))
        self.assertEqual(self.horiz1.get_p2(), (10, 4))
        
    def test_move(self):
        for i in range(10):
            self.horiz1.move()
            self.assertEqual(self.horiz1.get_p1(), (5 + i, 4))
            self.assertEqual(self.horiz1.get_p2(), (11 + i, 4))
            
    def test_turn(self):
        self.horiz1.turn(45 * 0.01745329251)
        self.assertLessEqual(abs(self.horiz1.p2[0] - 8.24264068712), .000001)
        self.assertLessEqual(abs(self.horiz1.p2[1] - 8.24264068712), .000001)
        self.assertEqual(self.horiz1.get_p2(), (8, 8))
        
    def test_get_boundary(self):
        self.assertEqual(
            self.horiz1.get_bounding_points(), 
            [(2, 2), (12, 2), (2, 6), (12, 6)])
        
    def test_check_collision(self):
        horiz2 = Bullet(4, 10, 0, 1)
        self.assertFalse(self.horiz1.check_collision(horiz2))
        self.assertFalse(horiz2.check_collision(self.horiz1))

        horiz3 = Bullet(5, 4, 0, 1)
        self.assertTrue(self.horiz1.check_collision(horiz3))
        self.assertTrue(horiz3.check_collision(self.horiz1))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()