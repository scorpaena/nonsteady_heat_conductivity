from matplotlib import cm
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
from geometry_properties import grid_map


def plot_3d(layers, time_array, T_output, T_bulk):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Make the data
    x = grid_map(layers) * 1e3
    y = time_array
    x, y = np.meshgrid(x, y)
    z = T_output

    # Plot the surface
    surf = ax.plot_surface(x, y, z, cmap=cm.jet)
    # Customize x axis
    loc = ticker.MultipleLocator(base=1e3*max(grid_map(layers))/4)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
    ax.set_xlabel('thickness, mm', fontsize=8)

    # Customize y axis
    loc = ticker.MultipleLocator(base=max(time_array) / 4)
    ax.yaxis.set_major_locator(loc)
    form = '%.1f' if max(time_array) < 4 else '%.0f'
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(form))
    ax.set_ylabel('time, sec.', fontsize=8)

    # Customize z axis
    ax.set_zlim(min(T_bulk), max(T_bulk))
    ax.set_zlabel('temperature, \u2103', fontsize=8)

    # Add a color bar which maps values to colors
    cb = plt.colorbar(surf, shrink=0.5, aspect=10, pad=0.08)
    cb.set_label('\u2103', y=1, rotation=0)

    plt.show()
