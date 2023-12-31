import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class Report:
    def __init__(self, spec_settings, width=18, height=30, hspace=0.1, wspace=0.1):
        self.spec_settings = spec_settings
        self.axes_dict = {}
        self.width = width
        self.height = height
        self.hspace = hspace
        self.wspace = wspace
        self.fig = plt.figure(figsize=(width, height))
        self.create_grid()

    def create_grid(self):
        gs = GridSpec(self.spec_settings['rows'], self.spec_settings['columns'], figure=self.fig, hspace=self.hspace, wspace = self.wspace)

        for subplot_name, axes_settings in self.spec_settings['axes'].items():
            row, col = axes_settings.get('position', (0, 0))
            rowspan, colspan = axes_settings.get('span', (1, 1))
            
            self.axes_dict[subplot_name] = self.fig.add_subplot(gs[row:row+rowspan, col:col+colspan])

    def show(self):
        plt.show()