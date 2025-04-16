import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap

def extract_pressure_grid(mesh):
    ny = len(mesh.p_nodes)
    nx = len(mesh.p_nodes[0])

    X = np.zeros((ny, nx))
    Y = np.zeros((ny, nx))
    P = np.zeros((ny, nx))

    for j in range(ny):
        for i in range(nx):
            node = mesh.p_nodes[j][i]
            X[j, i] = node.position[0]  # x
            Y[j, i] = node.position[1]  # y
            P[j, i] = node.p        # pressure

    return X, Y, P

def plot_filled_contour(X, Y, field, title="Filled Contour Field", save=True):
    red_blue_cmap = LinearSegmentedColormap.from_list("red_blue", ["blue", "white", "red"])

    fig, ax = plt.subplots(figsize=(15, 6))
    cp = ax.contourf(X, Y, field, levels=100, cmap=red_blue_cmap)

    cbar = fig.colorbar(cp, ax=ax, shrink=.25, aspect=5, pad=0.02)
    cbar.set_label(title)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)

    ax.set_xlim(X.min(), X.max())
    ax.set_ylim(0, .01)
    ax.set_aspect('equal')
    # ax.invert_xaxis()

    fig.tight_layout()

    if save:
        filename = title.lower().replace(" ", "_") + ".png"
        fig.savefig(filename, dpi=300)
        print(f"Saved: {filename}")

    # plt.show()

def extract_u_velocity_grid(mesh):
    ny = len(mesh.u_nodes)
    nx = len(mesh.u_nodes[0])

    X = np.zeros((ny, nx))
    Y = np.zeros((ny, nx))
    U = np.zeros((ny, nx))

    for j in range(ny):
        for i in range(nx):
            node = mesh.u_nodes[j][i]
            if node is not None:
                X[j, i] = node.position[0]
                Y[j, i] = node.position[1]
                U[j, i] = node.u
    return X, Y, U

def extract_v_velocity_grid(mesh):
    ny = len(mesh.v_nodes)
    nx = len(mesh.v_nodes[0])

    X = np.zeros((ny, nx))
    Y = np.zeros((ny, nx))
    V = np.zeros((ny, nx))

    for j in range(ny):
        for i in range(nx):
            node = mesh.v_nodes[j][i]
            if node is not None:
                X[j, i] = node.position[0]
                Y[j, i] = node.position[1]
                V[j, i] = node.v
    return X, Y, V

def plot_pressure_centerline(X, Y, P):
    x_vals = np.linspace(X.min(), X.max(), 200)
    y_center = 0.5 * (Y.min() + Y.max())
    points = np.column_stack((X.flatten(), Y.flatten()))
    values = P.flatten()
    centerline_pressure = griddata(points, values, (x_vals, np.full_like(x_vals, y_center)))

    plt.figure()
    plt.plot(x_vals, centerline_pressure, '-o')
    plt.xlabel('X')
    plt.ylabel('Pressure')
    plt.title(f'Pressure Along Channel Centerline (y = {y_center:.4f})')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_convergence(residuals):
    plt.figure()
    for key, values in residuals.items():
        plt.semilogy(values, label=key)
    plt.xlabel('Iteration')
    plt.ylabel('Residual (log scale)')
    plt.title('Convergence History')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
