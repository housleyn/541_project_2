class SIMPLEBase:
    def __init__(self, mesh, boundary, material):
        self.mesh = mesh
        self.boundary = boundary
        self.rho = material.rho
        self.mu = material.mu
        self.alphau = 0.5
        self.alphav = 0.5
        self.alphap = 0.5
        self.max_iterations = None
        self.iteration = 0

    