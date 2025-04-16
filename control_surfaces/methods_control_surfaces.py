class ControlSurfaceMethods: 

    def calculate_x_coefficients(self, mu, rho, dx, dy , alphau, pe, pw, uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old,j,ny):
        
        Fe = rho / 2 * (uE_old + self.u_old)
        Fw = rho / 2 * (uW_old + self.u_old)
        Fn = rho / 2 * (vUL_old + vUR_old)
        Fs = rho / 2 * (vBL_old + vBR_old)

        De = Dw = mu / dx
        Dn = Ds = mu / dy

        if j == 0:
            self.aE = De * dy + max(-Fe, 0) * dy
            self.aW = Dw * dy + max(Fw, 0) * dy
            Fn = rho / 2 * (vBL_old + vBR_old)
            Fs = rho / 2 * (vUL_old + vUR_old)
            self.aS = Ds * dx + max(Fs, 0) * dx

            self.aN = Dn * dx + max(-Fn, 0) * dx

            self.aP = ((self.aE + self.aW + 0 + self.aS + (Fe - Fw) * dy + (Fn - Fs) * dx)+mu*dx/(.5*dy)) /alphau
            self.b = (((pw - pe) * dy + ((1 - alphau) * self.aP / alphau) * self.u_old))*alphau
            
          

        elif j == ny - 1:
            self.aE = De * dy + max(-Fe, 0) * dy
            self.aW = Dw * dy + max(Fw, 0) * dy
            Fn = rho / 2 * (vBL_old + vBR_old)
            Fs = rho / 2 * (vUL_old + vUR_old)
            self.aN = Dn * dx + max(-Fn, 0) * dx

            self.aS = Dn * dx + max(Fn, 0) * dx
            self.aP = ((self.aE + self.aW + self.aN + 0 + (Fe - Fw) * dy + (Fn - Fs) * dx)+mu*dx/(.5*dy)) /alphau
            self.b = (((pw - pe) * dy + ((1 - alphau) * self.aP / alphau) * self.u_old))*alphau
            
            
            
            

        else:

            self.aE = De * dy + max(-Fe, 0) * dy
            self.aW = Dw * dy + max(Fw, 0) * dy
            self.aN = Dn * dx + max(-Fn, 0) * dx
            self.aS = Ds * dx + max(Fs, 0) * dx

            self.aP = (self.aE + self.aW + self.aN + self.aS + (Fe - Fw) * dy + (Fn - Fs) * dx)/alphau
            self.b = ((pw - pe) * dy + ((1 - alphau) * self.aP / alphau) * self.u_old)*alphau



    def calculate_y_coefficients(self, mu, rho, dx, dy, alphav, ps, pn, vN_old, vS_old, uUL, uUR, uBL, uBR):
        
        Fe = rho / 2 * (uUR + uBR)
        Fw = rho / 2 * (uUL + uBL)
        Fn = rho / 2 * (self.v_old + vN_old)
        Fs = rho / 2 * (self.v_old + vS_old)
        De = Dw = mu / dx
        Dn = Ds = mu / dy
        self.aE = De * dy + max(-Fe, 0) * dy
        self.aW = Dw * dy + max(Fw, 0) * dy
        self.aN = Dn * dx + max(-Fn, 0) * dx
        self.aS = Ds * dx + max(Fs, 0) * dx
        self.aP = (self.aE + self.aW + self.aN + self.aS + (Fe - Fw) * dy + (Fn - Fs) * dx)/alphav
        self.b = ((ps - pn) * dx + ((1 - alphav) * self.aP / alphav) * self.v_old)*alphav