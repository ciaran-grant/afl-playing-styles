
def load_display_options(max_rows=999, max_columns = 999):
    
    import pandas as pd
    pd.options.display.max_rows = max_rows
    pd.options.display.max_columns = max_columns
    
def ignore_warnings():
    
    import warnings
    warnings.filterwarnings('ignore')