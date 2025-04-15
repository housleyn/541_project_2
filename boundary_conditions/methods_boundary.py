class BoundaryMethods:
    def apply_pressure_boundary(self, side, value):
        nodes = self.mesh.get_boundary_nodes(side, 'p')
        for node in nodes:
            node.p_old= node.p = value
            node.aP = 1
            node.aE = node.aW = 0
            node.b = value
        self.conditions[side]['pressure'] = value

    def apply_velocity_boundary(self, side, u_value=None, v_value=None):
        if side in ['left', 'right']:
            field = 'u'
        elif side in ['top', 'bottom']:
            field = 'v'
        nodes = self.mesh.get_boundary_nodes(side, field)
        for node in nodes:
            if u_value is not None:
                node.u = node.u_old = u_value
            if v_value is not None:
                node.v = node.v_old = v_value
        self.conditions[side]['u'] = u_value
        self.conditions[side]['v'] = v_value


