class BoundaryBase:
    def __init__(self, mesh):
        
        self.mesh = mesh 
        self.conditions = {
            'left': {},
            'right': {},
            'top': {},
            'bottom': {}
        }
        self.conditions['left']['pressure'] = None
        self.conditions['right']['pressure'] = None
        self.conditions['top']['pressure'] = None
        self.conditions['bottom']['pressure'] = None
        self.conditions['left']['u'] = None
        self.conditions['left']['v'] = None
        self.conditions['right']['u'] = None
        self.conditions['right']['v'] = None
        self.conditions['top']['u'] = None
        self.conditions['top']['v'] = None
        self.conditions['bottom']['u'] = None
        self.conditions['bottom']['v'] = None
        
    