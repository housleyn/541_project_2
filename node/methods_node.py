class NodeMethods:
    def define_pressure_correction_coefficients(self, rho, dx, dy, uE, uW, vN, vS, dE, dW, dN, dS):
        
        self.aE = rho * dE * dy
        self.aW = rho * dW * dy
        self.aN = rho * dN * dx 
        self.aS = rho * dS * dx

        self.aP = self.aE + self.aW + self.aN + self.aS

        self.b = rho * (-uE*dy + uW*dy - vN*dx + vS*dx)