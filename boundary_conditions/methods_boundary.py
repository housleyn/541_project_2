class BoundaryMethods:
    def apply_pressure_boundary(self, side, value):
        nodes = self.mesh.get_boundary_nodes(side)
        for node in nodes:
            node.p_old = value
            node.aP = 1
            node.aE = node.aW = 0
            node.b = value
        self.conditions[side]['pressure'] = value

    def apply_velocity_boundary(self, side, u_value=None, v_value=None):
        nodes = self.mesh.get_boundary_nodes(side)
        for node in nodes:
            if u_value is not None:
                node.u = u_value
                node.u_fixed = True
            if v_value is not None:
                node.v = v_value
                node.v_fixed = True
        self.conditions[side]['u'] = u_value
        self.conditions[side]['v'] = v_value

    def apply_no_slip_wall(self, side):
        self.apply_velocity_boundary(side, u_value=0.0, v_value=0.0)
