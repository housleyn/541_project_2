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
        pass


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
