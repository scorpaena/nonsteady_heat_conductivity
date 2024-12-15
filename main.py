import numpy as np
from heat_properties import HeatProperties
from geometry_properties import get_nodes_amount, get_spans_number
from output import pyvista_plot_3d, matplotlib_plot_3d
from stpyvista import stpyvista as stv
import streamlit as st
import constants as c
from logging import getLogger

logger = getLogger(__name__)


iron = HeatProperties('iron')
copper = HeatProperties('copper')
layers_order = [iron, copper]

st.set_page_config(layout='wide')

col1, col2, col3 = st.columns([0.75, 0.25, 1])
with col1:
    scheme = st.radio(
        "Choose heat transfer configuration:",
        ["HEAT -> iron -> copper", "HEAT -> copper -> iron"],
    )
    st.write("\n")

    iron_layer_thickness = st.slider(f'Thickness of the `{iron}` layer (mm):', min_value=5, max_value=100, value=10, step=1)
    st.write("\n")

    copper_layer_thickness = st.slider(f'Thickness of the `{copper}` layer (mm):', min_value=5, max_value=100, value=10, step=1)
    st.write("\n")

    TIME = st.slider('Input heat exposure time (seconds):', min_value=5, max_value=60, value=10, step=1)

# layer thicknesses
layers = [0.001 * iron_layer_thickness, 0.001 * copper_layer_thickness]
if scheme == "HEAT -> copper -> iron":
    layers_order = [copper, iron]
    layers = [0.001 * copper_layer_thickness, 0.001 * iron_layer_thickness]

nodes_amount = get_nodes_amount(layers)

#coeffs for the canonical system of equation
alfa = nodes_amount * [0]
beta = nodes_amount * [0]

spans_number = get_spans_number(layers)

h = [layers[0]/spans_number, layers[1]/spans_number] #spatial pitch

T = nodes_amount * [c.T_initial] #current temperature
T_bulk = [] #temperature matrix needed for the output plots

time = 0 #total time
tau = c.tau #time pitch
time_array = [] #total time array needed for the output plots

while time <= TIME:
    time_array.append(time)
    T_bulk += T

    for i in range(nodes_amount):
        # Determine layer index
        j = 0 if i < spans_number else 1

        # Boundary condition at the first node
        Bi_0 = layers_order[0].Bi(alfa=layers_order[0].convective_heat_transfer_coefficient, h=h[0], heat_conductivity=layers_order[0].get_thermal_conductivity(T[0]))
        alfa[0] = 1 / (1 + Bi_0)
        beta[0] = Bi_0 * c.T_heat / (1 + Bi_0)

        # Conductivity values for layers
        a0 = layers_order[0].get_thermal_conductivity(T[i])
        a1 = layers_order[1].get_thermal_conductivity(T[i])

        # Heat transfer coefficients for current layer
        ai = layers_order[j].get_specific_heat(T[i]) / (h[j] ** 2)
        bi = (2 * ai + layers_order[j].density * layers_order[j].get_specific_heat(T[i]) / tau)
        ci = ai
        fi = -layers_order[j].density * layers_order[j].get_specific_heat(T[i]) * T[i] / tau

        # Recurrence relations for alpha and beta
        alfa[i] = ai / (bi - ci * alfa[i - 1])
        beta[i] = (ci * beta[i - 1] - fi) / (bi - ci * alfa[i - 1])

        # Boundary condition at the interface between layers
        numerator_alpha = 2 * a0 * a1 * tau * layers_order[1].get_thermal_conductivity(T[i])
        denominator_alpha = (
                2 * a0 * a1 * tau * (layers_order[1].get_thermal_conductivity(T[i]) +
                                     layers_order[0].get_thermal_conductivity(T[i]) * (1 - alfa[spans_number - 2]))
                + (h[j] ** 2) * (a0 * layers_order[1].get_thermal_conductivity(T[i]) +
                                 a1 * layers_order[0].get_thermal_conductivity(T[i]))
        )
        alfa[spans_number] = numerator_alpha / denominator_alpha

        numerator_beta = (
                2 * a0 * a1 * tau * layers_order[0].get_thermal_conductivity(T[i]) * beta[spans_number - 2] +
                (h[j] ** 2) * (a0 * layers_order[1].get_thermal_conductivity(T[i]) +
                               a1 * layers_order[0].get_thermal_conductivity(T[i])) * T[spans_number - 1]
        )
        beta[spans_number] = numerator_beta / denominator_alpha

        # Boundary condition at the last node
        Bi_N = layers_order[1].Bi(alfa=layers_order[1].convective_heat_transfer_coefficient, h=h[1], heat_conductivity=layers_order[1].get_thermal_conductivity(T[nodes_amount - 1]))
        T[nodes_amount - 1] = (Bi_N * c.T_ambient + T[nodes_amount - 2]) / (1 - Bi_N)

    # Backward substitution to compute temperature at all nodes
    for i in range(nodes_amount - 2, -1, -1):
        T[i] = alfa[i] * T[i + 1] + beta[i]

    # Increment time
    time += tau

a, b = int(len(T_bulk)/nodes_amount), nodes_amount  #rows, columns for .reshape
T_output = np.array(T_bulk)
T_output = T_output.reshape(a, b)
time_array = np.array(time_array)

with col3:
    st.pyplot(matplotlib_plot_3d(layers, time_array, T_output, T_bulk))
