#parameters are being returned from exe.py module
LAYER_THICKESS = [0, 0] #layers thickness
TIME = 0 #heat exposure time

tau = 0.5 #time pitch

#thermal emissivity
# thermal_emissivity_internal = 1600
# thermal_emissivity_external = 140
# thermal_emissivity = [thermal_emissivity_internal, thermal_emissivity_external]

T_heat = 1073 #heat temperature inside from the hot side
T_ambient = 303 #ambient temperature (air, room, etc.)
T_initial = 293 #initial temperature of the metall (i.e. inner surface)

MATERIALS = {
    'iron': {
        'density': 7680,
        'convective_heat_transfer_coefficient': 140,
        'specific_heat_curve_id': 'spl_MiG6mpKhbRqa',
        'thermal_conductivity_curve_id': 'spl_ddmQkxBmv9iT',
    },
    'copper': {
        'density': 8900,
        'convective_heat_transfer_coefficient': 1600,
        'specific_heat_curve_id': 'spl_2WXQfadWt7wa',
        'thermal_conductivity_curve_id': 'spl_RqqGq2ZpZ0Vg',
    },
}
