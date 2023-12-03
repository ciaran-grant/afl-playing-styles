import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Report:
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
    
    def create_subplots(self):
        """
        
        Example:
        match_report = Report(rows=3, cols=3)
        match_report.create_subplots()

        plot_expected_score_map(match_report.axs[0, 0])
        plot_possession_chart(match_report.axs[1, 1])
        plot_expected_vaep_plot(match_report.axs[2, 2])
        
        """
        self.fig, self.axs = plt.subplots(self.rows, self.cols, figsize = (self.width, self.height))
        
    def create_gridspec(self, spec_settings):
        
        """
        Example:
        match_report = Report(rows=3, cols=3, height = 48)
        spec_setting = {'home': (4, 1), 'details': (3, 1), 'away': (4, 1)}
        match_report.create_gridspec(spec_setting)

        # Home
        plot_expected_score_map(match_report.axs_dict['home'][0])
        plot_statistics_table(match_report.axs_dict['home'][1])
        plot_expected_score_map(match_report.axs_dict['home'][2])
        plot_expected_score_map(match_report.axs_dict['home'][3])
        # Details
        plot_expected_vaep_plot(match_report.axs_dict['details'][0])
        plot_possession_chart(match_report.axs_dict['details'][1])
        plot_expected_vaep_plot(match_report.axs_dict['details'][2])
        # Away
        plot_expected_vaep_plot(match_report.axs_dict['away'][0])
        plot_possession_chart(match_report.axs_dict['away'][1])
        plot_expected_vaep_plot(match_report.axs_dict['away'][2])
        plot_expected_vaep_plot(match_report.axs_dict['away'][3])
        """
        
        self.fig = plt.figure(figsize=(self.width, self.height), constrained_layout=True)
        self.gs = gridspec.GridSpec(self.rows, self.cols, figure=self.fig, hspace=self.hspace, wspace=self.wspace)

        home_gridspec = self.gs[0].subgridspec(spec_settings['home'][0], spec_settings['home'][1])
        home_axs = [self.fig.add_subplot(home_gridspec[i, :]) for i in range(spec_settings['home'][0])]

        details_gridspec = self.gs[1].subgridspec(spec_settings['details'][0], spec_settings['details'][1])
        details_axs = [self.fig.add_subplot(details_gridspec[i, :]) for i in range(spec_settings['details'][0])]

        away_gridspec = self.gs[2].subgridspec(spec_settings['away'][0], spec_settings['away'][1])
        away_axs = [self.fig.add_subplot(away_gridspec[i, :]) for i in range(spec_settings['away'][0])]

        self.fig.subplots_adjust(top=0.95, bottom=0.05)
        self.fig.tight_layout()

        self.axs_dict = {'home': home_axs, 'details': details_axs, 'away': away_axs}