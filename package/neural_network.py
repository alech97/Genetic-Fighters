'''
Created on Aug 23, 2017
This script handles the neural_network object
@author: Alec
'''

class Neural_Network(object):
    '''
    Neural Network class which represents a neural logic network 
    of varying size
    '''


    def __init__(self, num_input_nodes, weight_values, num_hidden_scalar, 
                 num_hidden_layers, num_output_nodes):
        '''
        Constructor for neural network of varying size.
        '''
        self.num_input_nodes = num_input_nodes
        self.weight_values = weight_values
        self.num_hidden_scalar = num_hidden_scalar
        self.num_output_nodes = num_output_nodes
        self.num_hidden_nodes_per_layer = int(
            round((num_input_nodes + num_output_nodes) * num_hidden_scalar))
        self.num_hidden_layers = num_hidden_layers
        self.hidden_nodes = [0] * self.num_hidden_nodes_per_layer
        
        #Assert weight_values is of correct size
        assert len(weight_values) == num_input_nodes * self.num_hidden_nodes_per_layer + \
            num_output_nodes * self.num_hidden_nodes_per_layer + \
            ((num_hidden_layers - 1) * self.num_hidden_nodes_per_layer * self.num_hidden_nodes_per_layer)
        
    def give_input_layer(self, input_layer):
        assert len(input_layer) == self.num_input_nodes
        #For each hidden node
        for i in range(self.num_hidden_nodes_per_layer):
            #Add the sum of magnitude of its links to each input node
            value = 0
            for x in range(self.num_input_nodes):
                value += input_layer[x] * self.weight_values[i * self.num_input_nodes + x]
            self.hidden_nodes[i] = value
        return self._receive_hidden_layers()
    
    def _receive_hidden_layers(self):
        index_shift = self.num_input_nodes * self.num_hidden_nodes_per_layer
        for extra_layer in range(self.num_hidden_layers - 1):
            #Assign new layer
            new_layer = [0] * self.num_hidden_nodes_per_layer
            for i in range(self.num_hidden_nodes_per_layer):
                value = 0
                for x in range(self.num_hidden_nodes_per_layer):
                    value += self.hidden_nodes[x] * self.weight_values[i * self.num_hidden_nodes_per_layer + x + index_shift]
                new_layer[i] = value
            
            #Make layer new "last" layer
            self.hidden_nodes = new_layer
            index_shift += self.num_hidden_nodes_per_layer * self.num_hidden_nodes_per_layer
        return self._receive_output_layer()
            
    def _receive_output_layer(self):
        output = [0] * self.num_output_nodes
        index_shift = self.num_hidden_nodes_per_layer * self.num_input_nodes + \
            ((self.num_hidden_layers - 1) * self.num_hidden_nodes_per_layer * self.num_hidden_nodes_per_layer)
        #For each output node
        for i in range(self.num_output_nodes):
            #Add the sum of magnitude of its links to each hidden node
            value = 0
            for x in range(self.num_hidden_nodes_per_layer):
                value += self.hidden_nodes[x] * self.weight_values[i * self.num_hidden_nodes_per_layer + x + index_shift]
            output[i] = value
        return output