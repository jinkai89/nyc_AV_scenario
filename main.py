import random
import networkx as nx
import matplotlib.pyplot as plt
from pyomo.environ import value
from model import optimize
import time

def get_data(n, edges, terminals):
    """This function puts the data in pyomo format"""
    data = {
        None: {
            'n': {None: n},
            'E': {None: edges + [(0, terminals[0])]},
            'cost': {1: 1,
  2: 1,
  3: 1,
  4: 1,
  5: 1,
  6: 1,
  7: 1,
  8: 1,
  9: 1,
  10: 1,
  11: 1,
  12: 1,
  13: 1,
  14: 1,
  15: 1,
  16: 1,
  17: 1,
  18: 1,
  19: 1,
  20: 1,
  21: 1,
  22: 1,
  23: 1,
  24: 1,
  25: 1},
            'utility': {1: 0.2,
  2: 0.45,
  3: 0.64741316,
  4: 0.86030383,
  5: 0.50251859,
  6: 0.89318027,
  7: 0.39961388,
  8: 0.72390638,
  9: 0.16240011,
  10: 0.5796534000000001,
  11: 0.05869445,
  12: 0.76489151,
  13: 0.67918328,
  14: 0.34088304,
  15: 0.20545594,
  16: 0.90865497,
  17: 0.71026246,
  18: 0.8474656999999999,
  19: 0.17186639,
  20: 0.73012258,
  21: 0.28420128,
  22: 0.33579929999999997,
  23: 0.21535504,
  24: 0.15886436,
  25: 0.18637036},
            'T': {None: terminals},
            'C': {None: 10},
        }
    }
    return data


def read_graph(filename):
    n = 0
    edges = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(int, line.split(','))
            n = max(n, max(x, y))
            edges.append((x, y))
    return n, edges


def read_coordinates(filename):
    coords = {}
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            v, x, y = map(int, line.split(','))
            coords[v] = (x, y)
    return coords


def plot(edges, terminals, coords):
    ax = plt.subplot()
    G = nx.Graph(edges)
    if terminals:
        G = G.subgraph(terminals)
    nx.draw_networkx(G, ax=ax, pos=coords,font_size = 8,node_size=125,edge_color='b',width =0.5,font_weight= 'bold')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    random.seed(12443549)
    ######################
    # hardcoded data
    # n = 24
    # edges = [
    #     (1, 2), (1, 3), (2, 1), (2, 6), (3, 1), (3, 4), (3, 12), (4, 3),
    #     (4, 5), (4, 11), (5, 4), (5, 6), (5, 9), (6, 2), (6, 5), (6, 8),
    #     (7, 8), (7, 18), (8, 6), (8, 7), (8, 9), (8, 16), (9, 5), (9, 8),
    #     (9, 10), (10, 9), (10, 11), (10, 15), (10, 16), (10, 17), (11, 4),
    #     (11, 10), (11, 12), (11, 14), (12, 3), (12, 11), (12, 13), (13, 12),
    #     (13, 24), (14, 11), (14, 15), (14, 23), (15, 10), (15, 14), (15, 19),
    #     (15, 22), (16, 8), (16, 10), (16, 17), (16, 18), (17, 10), (17, 16),
    #     (17, 19), (18, 7), (18, 16), (18, 20), (19, 15), (19, 17), (19, 20),
    #     (20, 18), (20, 19), (20, 21), (20, 22), (21, 20), (21, 22), (21, 24),
    #     (22, 15), (22, 20), (22, 21), (22, 23), (23, 14), (23, 22), (23, 24),
    #     (24, 13), (24, 21), (24, 23)
    # ]
    # terminals = [3, 5, 6]
    # n = 4
    # edges = [(1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)]
    # terminals = [3]
    # end of hardcoded data
    ######################
    # read and generate data
    start_time = time.time()
    n, edges = read_graph(r'C:\Users\owner\Documents\AV_Network_Paper\link_pair_simchi_levi.csv')
    coords = read_coordinates(r'C:\Users\owner\Documents\AV_Network_Paper\node_coordinate_simchi_levi_network.csv')
    plot(edges, None, coords)
    num_terminals = random.randint(1, n)
    terminals = [4]
    # solve problem
    instance = optimize(get_data(n, edges, terminals))
    # show solution
    new_terminals = []
    for i in instance.V:
        if value(instance.x[i]):
            print('Vertex {} is selected'.format(i))
            new_terminals.append(i)
    plot(edges, new_terminals, coords)
    cost = sum(instance.cost[i] * value(instance.x[i]) for i in instance.V)
    utility = sum(
        instance.utility[i] * value(instance.x[i]) for i in instance.V
    )
    print('Total cost: {}'.format(cost))
    print('Total utility: {}'.format(utility))
    print('Computation Time: %s seconds.'% (time.time() - start_time))
