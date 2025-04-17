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

def plot_mass_flow_convergence(mass_flow_log, x_target=0.025, save=True):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 5))
    plt.plot(range(len(mass_flow_log)), mass_flow_log, marker='o', linewidth=2)
    plt.xlabel("Iteration")
    plt.ylabel("Mass Flow at x = {:.3f} (kg/s)".format(x_target))
    plt.title("Mass Flow Rate Convergence")
    plt.grid(True)

    
    plt.savefig("mass_flow_convergence.png")
    





from plotting import extract_pressure_grid

def plot_pressure_centerline(mesh, y_target=0.005, save=True):
    from plotting import extract_pressure_grid
    X, Y, P = extract_pressure_grid(mesh)

    # Find closest row to y_target
    idx_row = np.argmin(np.abs(Y[:, 0] - y_target))
    x_line = X[idx_row, :]
    p_line = P[idx_row, :]

    plt.figure()
    plt.plot(x_line, p_line, marker='o')
    plt.xlabel("X (m)")
    plt.ylabel("Pressure (Pa)")
    plt.title(f"Pressure Along y = {Y[idx_row,0]:.5f} (Closest to {y_target})")
    plt.grid(True)
    
    plt.savefig("pressure_vs_x_centerline.png")
    # plt.show()



