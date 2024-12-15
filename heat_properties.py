from constants import MATERIALS
from splinecloud_scipy import load_spline
from functools import cache


class HeatProperties:

    def __init__(self, material):
        self.material = material
        self.density = MATERIALS[material]['density']
        self.convective_heat_transfer_coefficient = MATERIALS[material]['convective_heat_transfer_coefficient']
        self.specific_heat_curve_id = MATERIALS[material]['specific_heat_curve_id']
        self.thermal_conductivity_curve_id = MATERIALS[material]['thermal_conductivity_curve_id']

    def __str__(self):
        return self.material

    @staticmethod
    @cache
    def get_spline(curve_id):
        return load_spline(curve_id)

    def get_specific_heat(self, T):
        return self.get_spline(self.specific_heat_curve_id).eval(T)

    def get_thermal_conductivity(self, T):
        return self.get_spline(self.thermal_conductivity_curve_id).eval(T)

    def temperature_conductivity(self, heat_conductivity, heat_capacity):
        '''temperature conductivity coeff'''
        return heat_conductivity / (self.density * heat_capacity)

    def Fo(self, tau, h, heat_conductivity, heat_capacity):
        '''Fourier number'''
        return self.temperature_conductivity(heat_conductivity, heat_capacity) * tau / (h ** 2)

    def Bi(self, alfa, h, heat_conductivity):
        '''Biot number'''
        return alfa * h / heat_conductivity
