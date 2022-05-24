
from multiprocessing.sharedctypes import Value
import networkx as nx
import pandas as pd


class Salsa():
    """
    Class for implementing the web mining algorithm 'Stochastic Approach for Link-Structure Analysis' 
    """

    G = nx.DiGraph()
    HUB_NODES = 0
    AUTH_NODES = 0
    ITERATIONS = 1
    HUBS_VALUES = []
    AUTH_VALUES = []
    TEST_FILE = "./data/data_test_1.txt"
    TWITTER = "./data/twitter_combined.txt.gz"
    FACEBOOK = "./data/facebook_combined.txt.gz"
    GITHUB = "./data/musae_git_edges.csv"

    def __init__(self):
        """
        Initialization method for the class
        """
        self.nodes = []
        self.edges = []

    def read_data_from_txt(self):
        """
        Method used to read data from a TEST txt file"""
        with open(self.TEST_FILE, "r") as f:
            data = f.readlines()
            return data
    
    def _create_edges_from_txt(self):
        """
        Method to create the edges from data, networkpx automatically creates the nodes too
        """
        data = self.read_data_from_txt()
        for edge in data:
            [parent, child] = (edge.strip().split(','))
            self.G.add_edge(int(parent), int(child))
        return True

    def _create_edges_from_zip_csv(self):
        """
        Method used to write to create the directed graph from a .gz csv file
        """
        # twitter = pd.read_csv(self.TWITTER, compression='gzip', sep=' ', names=['start_node', 'end_node'])
        twitter = pd.read_csv(self.FACEBOOK, compression='gzip', sep=' ', names=['start_node', 'end_node'])
        # twitter = twitter.iloc[:1000]
        for i in range(len(twitter)):
            [parent, child] = [twitter.iloc[i,0], twitter.iloc[i, 1]]
            self.G.add_edge(int(parent), int(child))
        return True

    def _create_edges_from_csv(self):
        github = pd.read_csv(self.GITHUB)
        # github = github.iloc[:1000]
        for i in range(len(github)):
            [parent, child] = [github.iloc[i,0], github.iloc[i, 1]]
            self.G.add_edge(int(parent), int(child))
        return True

    def _add_hub_auth_values(self):
        # ---------1------------
        # If we read data from a txt file we use the _create_edges_from_txt method
        # self._create_edges_from_txt()

        #----------2------------    
        # If we read a zipped csv file with the .gz extension we use the _Create_edges_from_zip__csv method
        # self._create_edges_from_zip_csv()

        # ---------3------------
        # If we read a csv file wwe use the _Create_edges_from_zip__csv method
        self._create_edges_from_csv()

        for node in self.G.nodes:
            if self.G.out_edges(node):
                self.HUB_NODES += 1
            if self.G.in_edges(node):
                self.AUTH_NODES += 1

        for node in self.G.nodes:
            if self.G.out_edges(node):
                if self.G.in_edges(node):
                    self.G.add_node(node, data = {"Hub":1/self.HUB_NODES, "Auth":1/self.AUTH_NODES})
                else:
                    self.G.add_node(node, data = {"Hub":1/self.HUB_NODES, "Auth":0})
            elif self.G.in_edges(node):
                self.G.add_node(node, data = {"Hub":0, "Auth":1/self.AUTH_NODES})
        return True
        # print(self.G.nodes[2]["data"])

    def _compute_hub_value(self, node):
        """
        Method to compute the hub value of a node
        """
        hub_sum = 0
        node_data = self.G.nodes[node]["data"]
        hub_value = 0
        # print(hub_valu
        for edge in self.G.out_edges(node):
            in_v = len(self.G.in_edges(edge[1]))
            for in_edge in self.G.in_edges(edge[1]):
                out_w = len(self.G.out_edges(in_edge[0]))
                hub_value = self.G.nodes[in_edge[0]]["data"]["Hub"]
                hub_sum += hub_value/(in_v * out_w)
        self.G.nodes[node]["data"]["Hub"] = hub_sum
        return True

    def _compute_auth_value(self, node):
        """
        Method to compute the hub value of a node
        """
        auth_sum = 0
        node_data = self.G.nodes[node]["data"]
        auth_value = 0
        # print(hub_value)
        for edge in self.G.in_edges(node):
            out_v = len(self.G.out_edges(edge[0]))
            for out_edge in self.G.out_edges(edge[0]):
                in_w = len(self.G.in_edges(out_edge[1]))
                auth_value = self.G.nodes[out_edge[1]]["data"]["Auth"]
                auth_sum += auth_value/(out_v * in_w)
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
        return True

    def print_info(self):
        self.compute_salsa(self.ITERATIONS)
        for node in self.G.nodes(data=True):
            node_hub_value = node[1]["data"]["Hub"]
            self.HUBS_VALUES.append({f'node': node[0], 'Hub': node_hub_value})
            node_auth_value = node[1]["data"]["Auth"]
            self.AUTH_VALUES.append({f'node': node[0], 'Auth':node_auth_value})
            print(f'Node: {node[0]} -- Auth: {node_auth_value} -- Hub: {node_hub_value} ')
        # self.HUBS_VALUES = sorted(self.HUBS_VALUES, key = lambda x: x['node'])
        # self.AUTH_VALUES = sorted(self.AUTH_VALUES,  key = lambda x: x['node'], reverse=True)
        # print(f'Auths: {self.AUTH_VALUES} \n Hubs: {self.HUBS_VALUES}')

if __name__ == "__main__":
    salsa_class_inst = Salsa()
    salsa_class_inst.print_info()