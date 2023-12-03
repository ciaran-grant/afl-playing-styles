import numpy as np
from chain_utils import get_match, get_teams
from visualisation.afl_colours import team_colours

def get_expected_score_worm_data(chains, match_id):
    
    home_team, away_team = get_teams(match_id)
    match_chains = get_match(chains, match_id)
    match_scores = match_chains[~match_chains['xScore'].isna()]
    match_scores['net_xScore'] = np.where(match_scores['Team'] == home_team, match_scores['xScore'], -1*match_scores['xScore'])
    match_scores['cumsum_net_xScore'] = match_scores['net_xScore'].cumsum()
    
    return match_scores[['Duration', 'cumsum_net_xScore']]

def create_expected_score_worm_ax(ax, data, match_id):
    
    home_team, away_team = get_teams(match_id)
    
    ax.fill_between(data['Duration'], y1=data['cumsum_net_xScore'], where=(data['cumsum_net_xScore'] > 0), color = team_colours[home_team]['positive'])
    ax.fill_between(data['Duration'], y1=data['cumsum_net_xScore'], where=(data['cumsum_net_xScore'] < 0), color = team_colours[away_team]['positive'])

    biggest_lead = abs(data['cumsum_net_xScore']).max()
    ax.set_ylim(-biggest_lead-5, biggest_lead+5)  
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Expected Score Difference')
    
    return ax

def plot_expected_score_worm(ax, chain_data, match_id):
    
    match_scores = get_expected_score_worm_data(chain_data, match_id)
    ax = create_expected_score_worm_ax(ax, match_scores, match_id)
    
    return ax