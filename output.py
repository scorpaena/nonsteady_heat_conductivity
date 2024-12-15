from matplotlib import cm
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from geometry_properties import grid_map


def matplotlib_plot_3d(layers, time_array, T_output, T_bulk):
    fig = plt.figure(figsize=(12, 5))
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
    ax.xaxis.set_tick_params(labelsize=6)
    ax.set_xlabel('thickness, mm', fontsize=6)

    ax.set_facecolor('#0e1117')
    ax.figure.set_facecolor('#0e1117')

    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')


    # Customize y axis
    loc = ticker.MultipleLocator(base=max(time_array) / 4)
    ax.yaxis.set_major_locator(loc)
    form = '%.1f' if max(time_array) < 4 else '%.0f'
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(form))
    ax.set_ylabel('time, sec.', fontsize=6)
    ax.yaxis.label.set_color('white')
    ax.yaxis.set_tick_params(labelsize=6)
    ax.tick_params(axis='y', colors='white')

    # Customize z axis
    ax.set_zlim(min(T_bulk), max(T_bulk))
    ax.set_zlabel('temperature, K', fontsize=6)
    ax.zaxis.label.set_color('white')
    ax.zaxis.set_tick_params(labelsize=6)
    ax.tick_params(axis='z', colors='white')

    # Add a color bar which maps values to colors
    cb = plt.colorbar(surf, shrink=0.5, aspect=20, pad=0.1, orientation='vertical')
    cb.set_label('K', y=1, rotation=0, fontsize=6)
    cb.ax.yaxis.label.set_color('white')
    cb.ax.tick_params(axis='y', colors='white')
    cb.ax.yaxis.set_tick_params(labelsize=6)

    # plt.show()
    return fig


def pyvista_plot_3d(layers, time_array, T_output, T_bulk):
    x = grid_map(layers) * 1e3
    y = time_array
    x, y = np.meshgrid(x, y)
    z = T_output

    # Create the structured grid
    grid = pv.StructuredGrid(x, y, z)

    # Create the plotter
    plotter = pv.Plotter(window_size=[500, 500])

    # Add the data to the plotter
    plotter.add_mesh(
        grid,
        scalars=z.ravel(),
        cmap='jet',
        # scalars=grid.points[:, -1],
        show_edges=True,
        scalar_bar_args={'vertical': True}
    )
    plotter.view_isometric()
    plotter.set_background("#0e1117")
    plotter.show_axes()
    # plotter.set_scale(zscale=0.1)
    # plotter.set_scale(xscale=1, yscale=1, zscale=1)

    # Add a color bar
    plotter.add_scalar_bar('Temperature', shadow=True)

    # Show the plot
    return plotter
