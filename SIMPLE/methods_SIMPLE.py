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
        # b = np.flipud(b)
        b = np.flipud(b.reshape((4, 5))).flatten().reshape((20, 1))
        A = np.flip(A, axis=(0,1))
        print("A", A)
        print("b", b)
        # print('b shape', b.shape)
        
        
        # u_new = np.linalg.solve(A, b)
        # for j in range(self.mesh.ny):
        #     for i in range(self.mesh.nx + 1):
        #         self.mesh.u_nodes[j][i].u = u_new[j][i]
        
        return A,b


    def calculate_v_field(self):
        pass
    def calculate_p_prime_field(self):
        pass 
    def calculate_p_field(self):
        pass
    def calculate_new_u_field(self):
        pass 
    def calculate_new_v_field(self):
        pass
    def run(self):
        pass
