import numpy as np
class SIMPLEMethods:
    def generate_initial_guesses_u_field(self):
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx+1):  
                if self.mesh.u_nodes[j][i] is not None:
                    self.mesh.u_nodes[j][i].u_old = 0.001
    def generate_initial_guesses_v_field(self):
        for j in range(1, self.mesh.ny):  
            for i in range(self.mesh.nx + 2):
                self.mesh.v_nodes[j][i].v_old = 0.0001
    def generate_initial_guesses_p_field(self):
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx ):  
                self.mesh.p_nodes[j][i].p_old = 0.001

    def generate_initial_guesses(self):
        self.generate_initial_guesses_u_field()
        self.generate_initial_guesses_v_field()
        self.generate_initial_guesses_p_field()

    def calculate_u_field(self):
        for j in range(self.mesh.ny):
            self.mesh.u_nodes[j][0].aE = 0
            self.mesh.u_nodes[j][0].aW = 0
            self.mesh.u_nodes[j][0].aN = 0
            self.mesh.u_nodes[j][0].aS = 0
            self.mesh.u_nodes[j][0].aP = 1 
            self.mesh.u_nodes[j][0].b = 0.001
        for j in range(self.mesh.ny):
            for i in range(1,self.mesh.nx):
                uE_old = self.mesh.u_nodes[j][i+1].u_old
                uW_old = self.mesh.u_nodes[j][i-1].u_old
                vUL_old = self.mesh.v_nodes[j+1][i].v_old
                vUR_old = self.mesh.v_nodes[j+1][i+1].v_old
                vBL_old = self.mesh.v_nodes[j][i].v_old
                vBR_old = self.mesh.v_nodes[j][i+1].v_old
                pe = self.mesh.p_nodes[j][i].p_old
                pw = self.mesh.p_nodes[j][i-1].p_old
                
                self.mesh.u_nodes[j][i].calculate_x_coefficients(self.mu, self.rho, self.mesh.dx, self.mesh.dy, self.alphau, pe, pw, uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old,j, self.mesh.ny)
                    
        for j in range(self.mesh.ny):
            self.mesh.u_nodes[j][self.mesh.nx].aE = 0
            self.mesh.u_nodes[j][self.mesh.nx].aW = 1
            self.mesh.u_nodes[j][self.mesh.nx].aN = 0
            self.mesh.u_nodes[j][self.mesh.nx].aS = 0
            self.mesh.u_nodes[j][self.mesh.nx].aP = 1
            self.mesh.u_nodes[j][self.mesh.nx].b = 0
        A,b = self.mesh.build_matrix(self.mesh.u_nodes)
        
        b=b.reshape(-1,1)
        
        np.set_printoptions(precision=7, suppress=True, linewidth=200)
        
        u = np.linalg.solve(A, b)
        # Increase the last column of u values by 24.6% of the previous column values
        for j in range(self.mesh.ny):
            u[j * (self.mesh.nx + 1) + self.mesh.nx] += 0.246 * u[j * (self.mesh.nx + 1) + self.mesh.nx - 1]
 
        # Update the u_old values in the mesh
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx + 1):
                self.mesh.u_nodes[j][i].u = u[j * (self.mesh.nx + 1) + i]
        return A,b,u


    def calculate_v_field(self):

        for j in range(self.mesh.ny+1):
            self.mesh.v_nodes[j][0].aE = 0
            self.mesh.v_nodes[j][0].aW = 0
            self.mesh.v_nodes[j][0].aN = 0
            self.mesh.v_nodes[j][0].aS = 0
            self.mesh.v_nodes[j][0].aP = 1 
            self.mesh.v_nodes[j][0].b = 0
        for i in range(self.mesh.nx+2):
            self.mesh.v_nodes[0][i].aE = 0
            self.mesh.v_nodes[0][i].aW = 0
            self.mesh.v_nodes[0][i].aN = 0
            self.mesh.v_nodes[0][i].aS = 0
            self.mesh.v_nodes[0][i].aP = 1
            self.mesh.v_nodes[0][i].b = 0
            self.mesh.v_nodes[self.mesh.ny][i].aE = 0
            self.mesh.v_nodes[self.mesh.ny][i].aW = 0
            self.mesh.v_nodes[self.mesh.ny][i].aN = 0
            self.mesh.v_nodes[self.mesh.ny][i].aS = 0
            self.mesh.v_nodes[self.mesh.ny][i].aP = 1
            self.mesh.v_nodes[self.mesh.ny][i].b = 0
        for j in range(1,self.mesh.ny):
            for i in range(1,self.mesh.nx+1):
                vN_old = self.mesh.v_nodes[j+1][i].v_old
                vS_old = self.mesh.v_nodes[j-1][i].v_old
                uUL = self.mesh.u_nodes[j][i-1].u
                uUR = self.mesh.u_nodes[j][i].u
                uBL = self.mesh.u_nodes[j-1][i-1].u
                uBR = self.mesh.u_nodes[j-1][i].u
                ps = self.mesh.p_nodes[j-1][i-1].p_old
                pn = self.mesh.p_nodes[j][i-1].p_old

                self.mesh.v_nodes[j][i].calculate_y_coefficients(self.mu, self.rho, self.mesh.dx, self.mesh.dy, self.alphav, ps, pn, vN_old, vS_old, uUL, uUR, uBL, uBR)
                    
        for j in range(self.mesh.ny+1):
            self.mesh.v_nodes[j][self.mesh.nx+1].aE = 0
            self.mesh.v_nodes[j][self.mesh.nx+1].aW = 0
            self.mesh.v_nodes[j][self.mesh.nx+1].aN = 0
            self.mesh.v_nodes[j][self.mesh.nx+1].aS = 0
            self.mesh.v_nodes[j][self.mesh.nx+1].aP = 1 
            self.mesh.v_nodes[j][self.mesh.nx+1].b = 0
        
        A,b = self.mesh.build_matrix(self.mesh.v_nodes)
        
        b=b.reshape(-1,1)
        
        np.set_printoptions(precision=7, suppress=True, linewidth=200)

        v = np.linalg.solve(A, b)

        for j in range(self.mesh.ny+1):
            for i in range(self.mesh.nx+2):
                self.mesh.v_nodes[j][i].v = v[j * (self.mesh.nx + 2) + i]
        return A,b,v
    
    def calculate_p_prime_field(self):
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx):
                uE = self.mesh.u_nodes[j][i+1].u
                uW = self.mesh.u_nodes[j][i].u
                vN = self.mesh.v_nodes[j+1][i+1].v
                vS = self.mesh.v_nodes[j][i+1].v
                aE = self.mesh.u_nodes[j][i+1].aP * self.alphau
                aW = self.mesh.u_nodes[j][i].aP * self.alphau
                if j == 0:
                    aS = 1
                else:
                    aS = self.mesh.v_nodes[j][i+1].aP * self.alphav
                if j == self.mesh.ny - 1:
                    aN = 1
                else:
                    aN = self.mesh.v_nodes[j+1][i+1].aP * self.alphav
                
                dE = self.mesh.dy * self.alphav / aE
                dW = self.mesh.dy * self.alphav / aW
                dN = self.mesh.dx * self.alphau / aN
                dS = self.mesh.dx * self.alphau / aS


                self.mesh.p_nodes[j][i].define_pressure_correction_coefficients( self.rho, self.mesh.dx, self.mesh.dy,  uE, uW, vN, vS, dE, dW, dN, dS)
                
        A,b = self.mesh.build_matrix(self.mesh.p_nodes)
        b=b.reshape(-1,1)
        p_prime = np.linalg.solve(A, b)
        np.set_printoptions(precision=7, suppress=True, linewidth=200)
        print("p_prime Vector:")
        print(p_prime)
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx):
                self.mesh.p_nodes[j][i].p_prime = p_prime[j * (self.mesh.nx) + i]

                
    def calculate_p_field(self):
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx):
                self.mesh.p_nodes[j][i].p = self.mesh.p_nodes[j][i].p_old + self.alphap*self.mesh.p_nodes[j][i].p_prime
                self.mesh.p_nodes[j][i].p_old = self.mesh.p_nodes[j][i].p
    def calculate_new_u_field(self):
        for j in range(self.mesh.ny):
            for i in range(1,self.mesh.nx+1):
                pE = self.mesh.p_nodes[j][i].p
                pW = self.mesh.p_nodes[j][i-1].p
                d = self.mesh.dy  / (self.mesh.u_nodes[j][i].aP)
                self.mesh.u_nodes[j][i].u = self.mesh.u_nodes[j][i].u + d * (pW - pE)
                self.mesh.u_nodes[j][i].u_old = self.mesh.u_nodes[j][i].u

    def calculate_new_v_field(self):
        for j in range(1,self.mesh.ny):
            for i in range(1,self.mesh.nx+1):
                pN = self.mesh.p_nodes[j][i-1].p
                pS = self.mesh.p_nodes[j-1][i-1].p
                d = self.mesh.dx  / (self.mesh.v_nodes[j][i].aP)
                self.mesh.v_nodes[j][i].v = self.mesh.v_nodes[j][i].v + d * (pS - pN)
                self.mesh.v_nodes[j][i].v_old = self.mesh.v_nodes[j][i].v
    def run(self):
        self.generate_initial_guesses()
        while self.iteration < self.max_iterations:
            self.calculate_u_field()
            self.calculate_v_field()
            self.calculate_p_prime_field()
            self.calculate_p_field()
            self.calculate_new_u_field()
            self.calculate_new_v_field()
            self.iteration += 1
        
