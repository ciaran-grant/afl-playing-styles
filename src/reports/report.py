from abc import ABC, abstractclassmethod

class Report(ABC):
    def __init__(self,
                 rows: int,
                 cols: int,
                 height: int = 12,
                 width: int = 18,
                 hspace: float = 0.2,
                 wspace: float = 0.2
                 ):
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.hspace = hspace
        self.wspace = wspace
    
    @abstractclassmethod
    def create_subplots(self):
        pass
    
    @abstractclassmethod
    def create_gridspec(self):
        pass