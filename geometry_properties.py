import numpy as np


def get_spans_number(layers):
    """
    straight line equation is utilized
    as a method of finding number of spans
    """
    x0, x1 = 0.001, 1
    y0, y1 = 10, 1000
    return round((max(layers)-x0)*(y1-y0)/(x1-x0) + y0)


def get_nodes_amount(layers):
    """returns amount of nodes in len(c.s) layers"""
    spans_number = get_spans_number(layers)
    return len(layers) * spans_number + 1


def grid_map(layers):
    """divides sheet/plate into finite element grid"""
    x_axis = [0]
    spans_number = get_spans_number(layers)
    nodes_amount = get_nodes_amount(layers)  # amount of nodes in len(c.s) layers
    for i in range(nodes_amount-1):
        j = 0 if i <= spans_number-1 else 1
        x_axis.append(x_axis[i] + layers[j]/spans_number)
    return np.round(np.array(x_axis), 3)


# if __name__ == '__main__':
#     layers = [10, 20]
#     x = grid_map(layers)
#     for i in range(get_nodes_amount(layers)):
#         print(i, x[i])
