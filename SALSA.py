# import pandas as pd
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
# from random import randint
# import matplotlib


# twitter = pd.read_csv('twitter_combined.txt.gz', compression='gzip', sep=' ', names=['start_node', 'end_node'])
# twitter = twitter.iloc[0:1000]
# G = nx.from_pandas_edgelist(twitter, 'start_node', 'end_node')

# print(G)

import enum
import networkx as nx


class Salsa():
    """
    Class for implementing the web mining algorithm 'Stochastic Approach for Link-Structure Analysis' 
    """

    G = nx.DiGraph()
    TEST_FILE = "./data/data_test_1.txt"
    TWITTER = "twitter_combined.txt.gz"

    def __init__(self):
        """
        Initialization method for the class
        """
        self.nodes = []
        self.edges = []

    def read_data_from_txt(self):
        """
        Method used to read data from a txt file"""
        with open(self.TEST_FILE, "r") as f:
            data = f.readlines()
            return data
    
    def _create_edges(self):
        """
        Method to create the edges from data, networkpx automatically creates the nodes too"""
        data = self.read_data_from_txt()
        for edge in data:
            [parent, child] = (edge.strip().split(','))
            self.G.add_edge(int(parent), int(child))
        return True

    def _add_hub_auth_values(self):
        self._create_edges()
        for node in self.G.nodes:
            if self.G.out_edges(node):
                if self.G.in_edges(node):
                    self.G.add_node(node, data = {"Hub":1, "Auth":1})
                else:
                    self.G.add_node(node, data = {"Hub":1, "Auth":0})
            elif self.G.in_edges(node):
                self.G.add_node(node, data = {"Hub":0, "Auth":1})
        return True
        # print(self.G.nodes[2]["data"])

    def _compute_hub_value(self, node):
        """
        Method to compute the hub value of a node
        """
        hub_sum = 0
        node_data = self.G.nodes[node]["data"]
        hub_value = node_data["Hub"]
        # print(hub_value)
        for edge in self.G.out_edges(node):
            in_v = len(self.G.in_edges(edge[1]))
            for in_edge in self.G.in_edges(edge[1]):
                out_w = len(self.G.out_edges(in_edge[0]))
                hub_sum += hub_value/(in_v * out_w)
        self.G.nodes[node]["data"]["Hub"] = hub_sum
        return True

    def _compute_auth_value(self, node):
        """
        Method to compute the hub value of a node
        """
        auth_sum = 0
        node_data = self.G.nodes[node]["data"]
        auth_value = node_data["Auth"]
        # print(hub_value)
        for edge in self.G.in_edges(node):
            in_v = len(self.G.out_edges(edge[0]))
            for in_edge in self.G.out_edges(edge[0]):
                out_w = len(self.G.in_edges(in_edge[1]))
                auth_sum += auth_value/(in_v * out_w)
        self.G.nodes[node]["data"]["Auth"] = auth_sum
        return True

    def compute_salsa(self, iterations = 10):
        self._add_hub_auth_values()
        for i in range(iterations):
            for node in self.G.nodes:
                if self.G.out_edges(node):
                    self._compute_hub_value(node)
                if self.G.in_edges(node):
                    self._compute_auth_value(node)
        print(self.G.nodes[1]["data"])           

if __name__ == "__main__":
    class_inst = Salsa()
    class_inst.compute_salsa(10)

