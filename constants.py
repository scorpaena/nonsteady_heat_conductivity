#parameters are being returned from exe.py module
LAYER_THICKESS = [0, 0] #layers thickness
TIME = 0 #heat exposure time

def n(s):
    '''    
    straight line equation is utilized
    as a method of finding number of spans i.e. n=f(s)
    '''
    x0, x1 = 0.001, 1
    y0, y1 = 10, 1000
    return round((max(s)-x0)*(y1-y0)/(x1-x0) + y0)

spans_number = n(LAYER_THICKESS) #number of spans, per each layer

tau = 0.5 #time pitch

#thermal emissivity
alfaInternal = 1600
alfaExternal = 140
alfa = [alfaInternal, alfaExternal]

T_heat = 800 #heat temperature inside from the hot side
T_ambient = 30 #ambient temperature (air, room, etc.)
T_initial = 20 #initial temperature of the metall (i.e. inner surface)
