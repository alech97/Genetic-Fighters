'''
Created on Aug 24, 2017
Tests the neural_network module for correct networks.
@author: Alec Helyar
'''
import unittest
from package.neural_network import *


class Test(unittest.TestCase):


    def setUp(self):
        self.n1 = Neural_Network(3, [.5, .5, .5, .5, .5, .5, .5, .5], .5, 1, 1)
        self.n2 = Neural_Network(6, [0,1,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,0,1], .45, 1, 3)
        self.n3 = Neural_Network(3, [1,0,1,0,1,0,1,1,1,0,1,1], .5, 2, 1)

    def tearDown(self):
        pass


    def test_Neural_Network(self):
        self.assertEquals([3.0], self.n1.give_input_layer([2, 3, 1]))
        self.assertEquals(self.n2.num_hidden_nodes_per_layer, 4)
        val = self.n2.give_input_layer([3, -1, 2, 6, 4, 5])
        self.assertEquals([24.0, 10.0, 11.0], val)
        self.assertEquals([11.0], self.n3.give_input_layer([3, 1, 2]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()