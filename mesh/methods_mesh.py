from node import Node
from control_surfaces import ControlSurface
import numpy as np
import matplotlib.pyplot as plt

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
        
    def build_matrix(self, nodes):
        rows = len(nodes)
        cols = len(nodes[0])
        N = rows * cols
        A = np.zeros((N, N))
        b = np.zeros(N)

        def idx(i,j):
            return j*cols + i
        
        for j in range(rows):
            for i in range(cols):
                print(f"Building matrix for node ({j}, {i})")
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
   
    def get_boundary_nodes(self, side, field):
 
        if field == 'p':
            nodes = self.p_nodes
            nx = self.nx
            ny = self.ny
        elif field == 'u':
            nodes = self.u_nodes
            nx = self.nx + 1
            ny = self.ny
        elif field == 'v':
            nodes = self.v_nodes
            nx = self.nx + 2
            ny = self.ny + 1
        else:
            raise ValueError("Invalid field: must be 'p', 'u', or 'v'")

        boundary_nodes = []

        if side == 'left':
            for j in range(ny):
                boundary_nodes.append(nodes[j][0])
        elif side == 'right':
            for j in range(ny):
                boundary_nodes.append(nodes[j][-1])
        elif side == 'bottom':
            for i in range(nx):
                boundary_nodes.append(nodes[0][i])
        elif side == 'top':
            for i in range(nx):
                boundary_nodes.append(nodes[-1][i])
        else:
            raise ValueError("Invalid side: must be 'left', 'right', 'top', or 'bottom'")

        return boundary_nodes
    
    

    def plot_nodes_with_indices(self):
        def extract_coords(nodes):
            return [(n.position[0], n.position[1], i, j) 
                    for j, row in enumerate(nodes) for i, n in enumerate(row)]

        p_coords = extract_coords(self.p_nodes)
        u_coords = extract_coords(self.u_nodes)
        v_coords = extract_coords(self.v_nodes)

        plt.figure(figsize=(10, 10))
        for x, y, i, j in p_coords:
            plt.plot(x, y, 'ro')
            plt.text(x, y, f'({j},{i})', color='r', fontsize=8)
        for x, y, i, j in u_coords:
            plt.plot(x, y, 'bo')
            plt.text(x, y, f'({j},{i})', color='b', fontsize=8)
        for x, y, i, j in v_coords:
            plt.plot(x, y, 'go')
            plt.text(x, y, f'({j},{i})', color='g', fontsize=8)

        plt.title("Mesh Nodes with Indices (Red=p, Blue=u, Green=v)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.axis("equal")
        plt.grid(True)
        plt.show()
