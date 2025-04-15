class MeshBase:
    def __init__(self, domain, nx,ny):
        self.nx = nx
        self.ny = ny
        self.domain = domain
        (self.x_min,self.x_max), (self.y_min,self.y_max) = self.domain.get_bounds()
        self.dx = (self.x_max-self.x_min) / nx
        self.dy = (self.y_max-self.y_min) / ny
        self.p_nodes = [[None for _ in range(self.nx)] for _ in range(self.ny)]
        self.u_nodes = [[None for _ in range(self.nx + 1)] for _ in range(self.ny)]
        self.v_nodes = [[None for _ in range(self.nx + 2)] for _ in range(self.ny + 1)]
