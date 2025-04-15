class BoundaryBase:
    def __init__(self, mesh):
        
        self.mesh = mesh 
        self.conditions = {
            'left': {},
            'right': {},
            'top': {},
            'bottom': {}
        }
    