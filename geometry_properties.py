import numpy as np
from constants import spans_number, LAYER_THICKESS


def get_nodes_amount(layers):
    ''' returns amount of nodes in len(c.s) layers '''
    return len(layers) * spans_number + 1

def grid_map(layers):
    ''' divides sheet/plate into finite element grid '''
    x_axis = [0]
    nodes_amount = get_nodes_amount(layers)  # amount of nodes in len(c.s) layers
    for node in range(nodes_amount-1):
        j = 0 if node <= spans_number-1 else 1
        x_axis.append(x_axis[node] + LAYER_THICKESS[j]/spans_number)
    return np.round(np.array(x_axis), 3)


if __name__ == '__main__':
    layers = [10, 20]
    x = grid_map(layers)
    for i in range(get_nodes_amount(layers)):
        print(i, x[i])
