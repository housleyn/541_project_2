class ControlSurfaceBase:
    def __init__(self):
        self.u = None
        self.v = None
        self.position = None
        self.b = 0.0
        self.aE = 0.0 
        self.aW = 0.0
        self.aN = 0.0
        self.aS = 0.0
        self.aP = 0.0
        self.u_old = 0.0
        self.v_old = 0.0