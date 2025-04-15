from node import Node
from control_surfaces import ControlSurface
import numpy as np

class MeshMethods:
    def construct_u_mesh(self):
        for j in range(self.ny):
            for i in range(self.nx + 1):
                node = ControlSurface()
                node.position = self.x_min + (i) * self.dx, self.y_min + (j + 0.5) * self.dy
                self.u_nodes[j][i] = node
        
    def construct_v_mesh(self):
        for j in range(self.ny + 1):
            for i in range(self.nx + 2):
                node = ControlSurface()
                node.position = self.x_min + (i-1)*self.dx + .5*self.dx, self.y_min + (j) * self.dy
                self.v_nodes[j][i] = node

    def construct_p_mesh(self):
        for j in range(self.ny):
            for i in range(self.nx):
                node = Node()
                node.position = self.x_min + (i + 0.5) * self.dx, self.y_min + (j + 0.5) * self.dy
                self.p_nodes[j][i] = node

    def construct_mesh(self):
        self.construct_u_mesh()
        self.construct_v_mesh()
        self.construct_p_mesh()
        
    def buil_matrix(self, nodes):
        rows = len(nodes)
        cols = len(nodes[0])
        N = rows * cols
        A = np.zeros((N, N))
        b = np.zeros(N)

        def idx(i,j):
            return j*cols + i
        
        for j in range(rows):
            for i in range(cols):
                node = nodes[j][i]
                k = idx(i,j)
                A[k][k] = node.aP
                b[k] = node.b
                if i> 0:
                    A[k][idx(i-1,j)] = -node.aW
                if i < cols - 1:
                    A[k][idx(i+1,j)] = -node.aE
                if j > 0:
                    A[k][idx(i,j-1)] = -node.aS
                if j < rows -1:
                    A[k][idx(i,j+1)] = -node.aN
        return A, b
