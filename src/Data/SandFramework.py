import numpy as np
from scipy.optimize import fsolve


#Note: A lot of this work is based on the final lines of code that are not commented out in the MATLAB script
# This code seems to be dependent on having access to a MAT file, though if this is too troublesome, there seems to
# be instructions on what to do to get the work manually, which seems to rely on a lot of the work done throughout the program.
# This may be a simpler avenue if reusing that data is feasible

# The following is incomplete and very rough. Clarification from the sponsor will be needed
class SandFramework:
    def __init__(self):
        #These likely need to be customizable, but are set here for now
        self.gammap = 7 #kN / m^3
        self.k0 = 0.5
        self.chmin = 0.0000031
        self.V50 = 1
    
    def root2d(self, func):
        # Used to store functions with different arrays
        function = np.zeros(2)

        function(1) = np.exp(-np.exp(-(func(0) + func(1)))) - func(1) * (1 + func(0) ** 2)
        function(2) = func(0) * np.cos(func(1)) + func(1) * np.sin(func(0)) - 0.5

        return function
    
    def pm(self, val, depr1):
        return self.gammap * ((1 + 2 * self.k0) / 3) * depr1(val)

    def V_func(self, val, Velr):
        #Velr = S202.velr (Presumably from mat file, though earlier portions of script specify way to solve using .bin information stored in Peak)
        return (Velr(val) * 0.04375) / self.chmin
    
    def strainterm(self, val):
        return 1 / (1 + (self.V_func(val) / self.V50))
    

    def relative_density(self):
        rd0 = np.full(71, 0.02)

        rd = fsolve(self.root2d, rd0)

        rd = rd * 100

        rd = rd.reshape(-1, 1)

        F = self.root2d(rd)

        #TODO: Load in, or pass the appropriate bLog matrix (MATLAB example is bLog07A3-1 1.mat), who puts spaces in file names?

        #Julie will need to be asked for an example file (preferably bLog07A3) to understand what specific data is needed here
        #This data should be held already in other classes

        depr1 = s202.Depth
        qdynr = s202.qdyn
        Velr = s202.velr

        # decr=s182.dec is commented out in MATLAB (Might still be used in edge cases)
        
        phicv = 34
        Q = 9
        R = 1
        Nkt = 12
        c0 = 300
        c1 = 0.46
        c2 = 2.96

        #F = cell(8, 1);
        #ct= 1;
        #within loop
        #rdarray(ct) = rd;

        #r=1;
        #rd1=zeros(55,6);

        #Note that Q is previously defined as 9. I do not know the relevance of that, so ensure with Julie this definition is correct
        for Q in range (5, 10):
            k = 1
            for j in range (10, depr1.size):
                #There is a lot used here that is not defined beforehand in seemingly used code. I was told only the non-commented out code was used, but that cannot be true
                qdynr(j)

                #This is a really gross equation that I will try to make look better here
                #The usage of this is also currently unknown to me
                F(k) = qdynr(j) - (((Nkt * 0.5 * ((6 * np.sin(phicv)) / (3 - np.sin(phicv))) * np.exp(Q - 1/rd(j)))) +
                                self.strainterm(j) * ((((c0 * (self.pm(j) ** c1) * np.exp(rd(j) * c2)) - (Nkt * 0.5 * ((6 * np.sin(phicv))
                                                                                                            / (3 - np.sin(phicv)))) * np.exp(Q - 1 / rd(j))))))
                
                #Here's the second, commented out, equation that will maybe be used eventually
                #F= qdynr(j) - (((Nkt * 0.5 * ((6 * np.sin(phicv)) / (3 - np.sin(phicv))) * np.exp(Q - 1 / rd))) + 
                #            self.strainterm(j) * ((((c0 * (self.pm(j) ** c1) * np.exp(rd * c2)) - (Nkt * 0.5 * ((6 * np.sin(phicv))
                #                                                                                        / (3 - np.sin(phicv)))) * np.exp(Q - 1 / rd)))))
                
                k = k+1
        
            #Relevance unknown, seems pointless
            #rd1[:, r] = rd[:, 0]


    
   