import numpy as np
class SIMPLEMethods:
    def generate_initial_guesses_u_field(self):
        for j in range(self.mesh.ny):
            for i in range(1,self.mesh.nx):
                self.mesh.u_nodes[j][i].u_old = .001
    def generate_initial_guesses_v_field(self):
        for j in range(1,self.mesh.ny-1):
            for i in range(self.mesh.nx+1):
                self.mesh.v_nodes[j][i].v_old = 0.0001
    def generate_initial_guesses_p_field(self):
        for j in range(self.mesh.ny):
            for i in range(self.mesh.nx-1):
                self.mesh.p_nodes[j][i].p_old = 0.001

    def generate_initial_guesses(self):
        self.generate_initial_guesses_u_field()
        self.generate_initial_guesses_v_field()
        self.generate_initial_guesses_p_field()

    def calculate_u_field(self):
        for j in range(self.mesh.ny-1):
            for i in range(1,self.mesh.nx):
                print(f"Calculating u field for node ({j}, {i})")
                uE_old = self.mesh.u_nodes[j][i+1].u_old
                uW_old = self.mesh.u_nodes[j][i-1].u_old
                vUL_old = self.mesh.v_nodes[j+1][i].v_old
                vUR_old = self.mesh.v_nodes[j+1][i+1].v_old
                vBL_old = self.mesh.v_nodes[j][i].v_old
                vBR_old = self.mesh.v_nodes[j][i+1].v_old
                pe = self.mesh.p_nodes[j][i].p_old
                pw = self.mesh.p_nodes[j][i-1].p_old
                self.mesh.u_nodes[j][i].calculate_x_coefficients(self.mu, self.rho, self.mesh.dx, self.mesh.dy, self.alphau, pe, pw, uE_old, uW_old, vUL_old, vUR_old, vBL_old, vBR_old)
        A,b = self.mesh.build_matrix(self.mesh.u_nodes)
        new_u = np.linalg.solve(A,b)
        for j in range(self.mesh.ny):
            for i in range(1, self.mesh.nx):
                idx = j * (self.mesh.nx - 1) + (i - 1)
                self.mesh.u_nodes[j][i].u = new_u[idx]
        return A, b

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
