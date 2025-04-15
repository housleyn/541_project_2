import numpy as np
import matplotlib.pyplot as plt

class DomainMethods:
    def define_lower_boundary(self, func):
        self.lower_boundary_func = func

    def define_upper_boundary(self, func):
        self.upper_boundary_func = func

    def define_left_boundary(self, func):
        self.left_boundary_func = func

    def define_right_boundary(self, func):
        self.right_boundary_func = func

    def get_bounds(self, x_samples=100, y_samples=100):
        self.x_min = self.left_boundary_func(0, 0)
        self.x_max = self.right_boundary_func(0, 0)
        x_vals = np.linspace(self.x_min, self.x_max, x_samples)
        y_lower_vals = np.array([self.lower_boundary_func(x, 0) for x in x_vals])
        y_upper_vals = np.array([self.upper_boundary_func(x, 0) for x in x_vals])
        y_min = min(y_lower_vals.min(), y_upper_vals.min())
        y_max = max(y_lower_vals.max(), y_upper_vals.max())
        return (self.x_min, self.x_max), (y_min, y_max)

    def plot_domain(self, x_range, y_range):
        x = np.linspace(x_range[0], x_range[1], 200)
        y_lower = np.array([self.lower_boundary_func(xi, 0) for xi in x])
        y_upper = np.array([self.upper_boundary_func(xi, 0) for xi in x])

        y_left_min = self.lower_boundary_func(x_range[0], 0)
        y_left_max = self.upper_boundary_func(x_range[0], 0)
        y_right_min = self.lower_boundary_func(x_range[1], 0)
        y_right_max = self.upper_boundary_func(x_range[1], 0)

        y_left = np.linspace(y_left_min, y_left_max, 200)
        y_right = np.linspace(y_right_min, y_right_max, 200)
        x_left = np.array([self.left_boundary_func(0, yi) for yi in y_left])
        x_right = np.array([self.right_boundary_func(0, yi) for yi in y_right])

        plt.plot(x, y_lower, 'k')
        plt.plot(x, y_upper, 'k')
        plt.plot(x_left, y_left, 'k')
        plt.plot(x_right, y_right, 'k')
        plt.xlim(x_range)
        plt.ylim(y_range)
        plt.axis('equal')
        plt.grid()