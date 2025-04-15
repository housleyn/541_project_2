class ControlSurfaceMethods: 
  
    def calculate_x_coefficients(self, dx, dy, Fe, Fw, Fn, Fs,pe, pw, alphau, mu, uN_old, uS_old, uE_old, uW_old):
        De = Dw = mu/dx
        Dn = Ds = mu/dy
        self.aE = De * dy + max(-Fe, 0)*dy 
        self.aW = Dw*dy + max(Fw,0)*dy 
        self.aN = Dn*dx + max(-Fn,0)*dx 
        self.aS = Ds*dx + max(Fs,0)*dx 
        self.aP = self.aE + self.aW + self.aN + self.aS + (Fe-Fw)*dy + (Fn-Fs)*dx 
        self.b = (pe-pw)*dy + ((1-alphau)*self.aP/alphau)*self.u_old

    def calculate_y_coefficients(self, dx, dy, De, Fe, Dw, Fw, Dn, Fn, Ds, Fs, ps, pn, alphav):
        self.aE = De * dy + max(-Fe, 0)*dy 
        self.aW = Dw*dy + max(Fw,0)*dy 
        self.aN = Dn*dx + max(-Fn,0)*dx 
        self.aS = Ds*dx + max(Fs,0)*dx
        self.aP = self.aE + self.aW + self.aN + self.aS + (Fe-Fw)*dy + (Fn-Fs)*dx 
        self.b = (ps-pn)*dx + ((1-alphav)*self.aP/alphav)*self.v_old