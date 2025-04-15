class ControlSurfaceMethods: 
  
    def calculate_x_coefficients(self, mu, rho, dx, dy , alphau, pe, pw, uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old):
        Fe = rho/2 * (uE_old + self.u_old)
        Fw = rho/2 * (uW_old + self.u_old)
        Fn = rho/2 * (vUL_old + vUR_old)
        Fs = rho/2 * (vBL_old + vBR_old)
        De = Dw = mu/dx
        Dn = Ds = mu/dy
        self.aE = De * dy + max(-Fe, 0)*dy 
        self.aW = Dw*dy + max(Fw,0)*dy 
        self.aN = Dn*dx + max(-Fn,0)*dx 
        self.aS = Ds*dx + max(Fs,0)*dx 
        self.aP = self.aE + self.aW + self.aN + self.aS + (Fe-Fw)*dy + (Fn-Fs)*dx 
        self.b = (pw-pe)*dy + ((1-alphau)*self.aP/alphau)*self.u_old

    def calculate_y_coefficients(self, mu, rho, dx, dy, alphav, ps, pn, vN_old, vS_old, uUL_old, uUR_old, uBL_old, uBR_old):
        De = Dw = mu/dx 
        Dn = Ds = mu/dy
        Fe = rho/2 * (uUR_old + uBR_old)
        Fw = rho/2 * (uUL_old + uBL_old)
        Fn = rho/2 * (vN_old + self.v_old)
        Fs = rho/2 * (vS_old + self.v_old)
        self.aE = De * dy + max(-Fe, 0)*dy 
        self.aW = Dw*dy + max(Fw,0)*dy 
        self.aN = Dn*dx + max(-Fn,0)*dx 
        self.aS = Ds*dx + max(Fs,0)*dx
        self.aP = self.aE + self.aW + self.aN + self.aS + (Fe-Fw)*dy + (Fn-Fs)*dx 
        self.b = (ps-pn)*dx + ((1-alphav)*self.aP/alphav)*self.v_old