import numpy as np
import scipy.optimize as opt
import constants as c


class heatProperties:

    def __init__(self, material, density):
        self.material = material
        self.density = density

    def _layerTempAssign(self):
        if self.material == 'Iron':
            T = [20,200,400,600,800]
        else:
            T = [20,100,300,600,900]
        return T
   
        
    def _layerLambdaAssign(self):    
        if self.material == 'Iron':
            lambda_ = [41,43,37,32,24]
        else:
            lambda_ = [395,392,373,344,321]
        return lambda_
    
    
    def _layerCapacityAssign(self):  
        if self.material == 'Iron':
            c_ = [469,519,553,611,703]
        else:
            c_ = [381,399,422,456,482]
        return c_

#==== Heat Conductivity System Solution Block ======
    def _heatConductSystem(self, initGuess):
        a0, a1, a2, a3, a4 = initGuess
        T = self._layerTempAssign()
        lambda_ = self._layerLambdaAssign()
        return (a0 + a1*T[0] + a2*T[0]**2 + a3*T[0]**3 + a4*T[0]**4 - lambda_[0],
                a0 + a1*T[1] + a2*T[1]**2 + a3*T[1]**3 + a4*T[1]**4 - lambda_[1],
                a0 + a1*T[2] + a2*T[2]**2 + a3*T[2]**3 + a4*T[2]**4 - lambda_[2],
                a0 + a1*T[3] + a2*T[3]**2 + a3*T[3]**3 + a4*T[3]**4 - lambda_[3],
                a0 + a1*T[4] + a2*T[4]**2 + a3*T[4]**3 + a4*T[4]**4 - lambda_[4])

    def _heatConductSystemSolution(self):
        initGuess = (0, 0, 0, 0, 0)
        systemOfEquation = self._heatConductSystem
        solution = opt.fsolve(systemOfEquation, initGuess)
        return solution
    
    def heatConduct(self, T):
        a = []
        aT = []
        for i in range(len(self._heatConductSystemSolution())):
            a.append(self._heatConductSystemSolution()[i])
            aT.append(a[i]*T**i)
        Lambda = sum(aT)
        return Lambda
#==== End of Heat Conductivity System Solution Block ======

#==== Heat Capacity System Solution Block ======  
    def _heatCapacSystem(self, initGuess):
        a0, a1, a2, a3, a4 = initGuess
        T = self._layerTempAssign()
        c_ =  self._layerCapacityAssign()
        return (a0 + a1*T[0] + a2*T[0]**2 + a3*T[0]**3 + a4*T[0]**4 - c_[0],
                a0 + a1*T[1] + a2*T[1]**2 + a3*T[1]**3 + a4*T[1]**4 - c_[1],
                a0 + a1*T[2] + a2*T[2]**2 + a3*T[2]**3 + a4*T[2]**4 - c_[2],
                a0 + a1*T[3] + a2*T[3]**2 + a3*T[3]**3 + a4*T[3]**4 - c_[3],
                a0 + a1*T[4] + a2*T[4]**2 + a3*T[4]**3 + a4*T[4]**4 - c_[4])

    def _heatCapacSystemSolution(self):
        initGuess = (0,0,0,0,0)
        systemOfEquation = self._heatCapacSystem
        solution = opt.fsolve(systemOfEquation,initGuess)
        return solution
        
    def heatCapac(self, T):
        a = []
        aT = []
        for i in range(len(self._heatCapacSystemSolution())):
            a.append(self._heatCapacSystemSolution()[i])
            aT.append(a[i]*T**i)
        Capacity = sum(aT)
        return Capacity
#==== End of Heat Capacity System Solution Block ======       
    
    def Fo(self, T, j, tau):
        '''Fourier number'''
        h = c.LAYER_THICKESS[j]/(c.spans_number)
        fo = (self.heatConduct(T)*tau)/(self.density*self.heatCapac(T)*h**2)
        return fo

    def Bi(self, T, j):
        '''Biot number'''
        h = c.LAYER_THICKESS[j]/(c.spans_number)
        bi = c.alfa[j]*h / self.heatConduct(T)
        return bi

    def tempConduct(self, T):
        '''temperature conductivity coeff'''
        tempConduct = self.heatConduct(T)/(self.density*self.heatCapac(T))
        return tempConduct

iron = heatProperties('Iron', 7680)
copper = heatProperties('Copper', 8933)

layer0 = iron
layer1 = copper

layers = []
