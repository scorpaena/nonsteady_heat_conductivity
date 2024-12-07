#parameters are being returned from exe.py module
LAYER_THICKESS = [0, 0] #layers thickness
TIME = 0 #heat exposure time

tau = 0.5 #time pitch

#thermal emissivity
alfaInternal = 1600
alfaExternal = 140
alfa = [alfaInternal, alfaExternal]

T_heat = 800 #heat temperature inside from the hot side
T_ambient = 30 #ambient temperature (air, room, etc.)
T_initial = 20 #initial temperature of the metall (i.e. inner surface)
