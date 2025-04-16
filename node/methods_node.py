class NodeMethods:
    def define_pressure_correction_coefficients(self, rho, dx, dy, uE, uW, vN, vS, dE, dW, dN, dS, i, j, nx, ny):
        # Compute raw coefficients
        aE = rho * dE * dy
        aW = rho * dW * dy
        aN = rho * dN * dx 
        aS = rho * dS * dx

        # Modifications for corner and near-corner nodes
        # Southwest corner
        if i == 0 and j == 0:
            aW = 0
        # Northwest corner
        elif i == 0 and j == ny - 1:
            aW = 0
        # Southeast near-corner
        elif i == nx - 2 and j == 0:
            aE = 0
        # Northeast near-corner
        elif i == nx - 2 and j == ny - 1:
            aE = 0

        # Assign adjusted values
        self.aE = aE
        self.aW = aW
        self.aN = aN
        self.aS = aS
        self.aP = aE + aW + aN + aS

        # b is always based on full imbalance (not modified)
        self.b = rho * (-uE * dy + uW * dy - vN * dx + vS * dx)
