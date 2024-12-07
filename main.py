import time as t
import numpy as np
import heat_properties as hP
import geometry_properties as gP
import constants as c


start = t.time()

N = gP.get_nodes_amount(c.LAYER_THICKESS)

#coeffs for the canonical system of equation
alfa = N * [0]
beta = N * [0]

h = [c.LAYER_THICKESS[0]/c.spans_number, c.LAYER_THICKESS[1]/c.spans_number] #spatial pitch

T = N*[c.T_initial] #current temperature
T_bulk = [] #temperature matrix needed for the output plots

time = 0 #total time
tau = c.tau #time pitch
timeArray = [] #total time array needed for the output plots

while time <= c.TIME:
    timeArray.append(time)
    T_bulk += T 
    for i in range(gP.get_nodes_amount(c.LAYER_THICKESS)):
        j = 0 if i < c.spans_number else 1
        

        alfa[0] = 1/(1+hP.layers[0].Bi(T[0],0))
        beta[0] = hP.layers[0].Bi(T[0],0)*c.T_heat/(1+hP.layers[0].Bi(T[0],0))

        a0 = hP.layers[0].tempConduct(T[i])
        a1 = hP.layers[1].tempConduct(T[i])

        ai = hP.layers[j].heatConduct(T[i])/(h[j]**2)
        bi = (2*hP.layers[j].heatConduct(T[i])/(h[j]**2)+hP.layers[j].density
             *hP.layers[j].heatCapac(T[i])/tau)
        ci = hP.layers[j].heatConduct(T[i])/(h[j]**2)
        fi = -hP.layers[j].density*hP.layers[j].heatCapac(T[i])*T[i]/tau
        
        alfa[i] = ai/(bi - ci * alfa[i-1])
        beta[i] = (ci*beta[i-1]-fi)/(bi-ci*alfa[i-1])

        alfa[c.spans_number] = (2*a0*a1*tau*hP.layers[1].heatConduct(T[i])/(2*a0*a1*tau
                      *(hP.layers[1].heatConduct(T[i])
                      +hP.layers[0].heatConduct(T[i])*(1-alfa[c.spans_number-2]))
                      +(h[j]**2)*(a0*hP.layers[1].heatConduct(T[i])
                      +a1*hP.layers[0].heatConduct(T[i]))))
       
        beta[c.spans_number] = ((2*a0*a1*tau*hP.layers[0].heatConduct(T[i])*beta[c.spans_number-2]
                      +(h[j]**2)*(a0*hP.layers[1].heatConduct(T[i])
                      +a1*hP.layers[0].heatConduct(T[i]))*T[c.spans_number-1])
                      /(2*a0*a1*tau*(hP.layers[1].heatConduct(T[i])
                      +hP.layers[0].heatConduct(T[i])*(1-alfa[c.spans_number-2]))
                      +(h[j]**2)*(a0*hP.layers[1].heatConduct(T[i])
                      +a1*hP.layers[0].heatConduct(T[i]))))
        
        T[N-1] = ((hP.layers[1].Bi(T[N-1],1)*c.T_ambient + T[N-2])
                    /(1-hP.layers[1].Bi(T[N-1],1)))

    for i in range(N-2,-1,-1):
        T[i] = alfa[i]*T[i+1]+beta[i]
    time += tau

a, b = int(len(T_bulk)/N), N  #rows, columns for .reshape
T_output = np.array(T_bulk)
T_output = T_output.reshape(a, b)
timeArray = np.array(timeArray)

end = t.time()
timeOfWaiting = round(end - start)
print('Total ' + str(timeOfWaiting) + ' sec. of waiting')

