from chain_utils import get_match, get_team, get_scores
import pandas as pd
import numpy as np
import seaborn as sns

def create_match_score_summary(match_summary):
    
    match_summary = get_scores(match_summary)
    
    home_match_summary = match_summary[['Home_Team', 'Home_Goals', 'Home_Behinds', 'Home_Score']]
    home_match_summary.columns = ['Team', 'Goals', 'Behinds', 'Score']

    away_match_summary = match_summary[['Away_Team', 'Away_Goals', 'Away_Behinds', 'Away_Score']]
    away_match_summary.columns = ['Team', 'Goals', 'Behinds', 'Score']
    
    match_score_summary = pd.concat([home_match_summary, away_match_summary])
    
    return match_score_summary

def create_match_statistics_data(player_stats, score_summary):
    
    match_stats = player_stats.groupby('Team').sum()[['Disposals', 'Effective_Disposals', 'Goal_Assists', 'Pressure_Acts', 'Shots_At_Goal', 'Possessions', 'xScore', 'exp_offensive_value',  'exp_vaep_value_received', 'xDisposal']].reset_index()
    match_stats = match_stats.merge(score_summary, how = 'left', left_on='Team', right_on='Team')
    match_stats = match_stats.set_index('Team').T.reset_index()
    match_stats.rename(columns={'index': 'Statistics'}, inplace=True)

    table_order = ['Score', 'xScore', 'Goals', 'Behinds', 'Shots_At_Goal', 'Goal_Assists', 'Possessions', 'Disposals', 'Effective_Disposals', 'xDisposal', 'exp_offensive_value', 'exp_vaep_value_received', 'Pressure_Acts']
    match_stats['Statistics'] = pd.Categorical(match_stats['Statistics'], categories=table_order, ordered=True)
    match_stats = match_stats.sort_values('Statistics').set_index('Statistics')
    
    return match_stats

def create_match_stats(summary, player_stats, match_id):
    
    match_summary = get_match(summary, match_id)
    match_player_stats = get_match(player_stats, match_id)
    match_score_summary = create_match_score_summary(match_summary)
    match_stats = create_match_statistics_data(match_player_stats, match_score_summary)

    return match_stats.astype(float)

def get_normalised_match_stats(match_stats):
    
    return match_stats.div(match_stats.sum(axis=1), axis=0)

def plot_heatmap(ax, data):
    
    heatmap = sns.heatmap(data, ax=ax, cbar=False, cmap = "coolwarm")

    ax.set_xticklabels(list(data.columns))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', which='both', top=False)

    ax.set_yticklabels(list(data.index))
    ax.tick_params(axis='y', which='both', left=False)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title('Match Statistics')
    
    return ax

def annotate_heatmap(ax, data):
    
    data_array = np.array(data)
    annotations = [["{:.0f}", "{:.0f}"], 
                ["{:.1f}", "{:.1f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"],
                ["{:.0f}", "{:.0f}"], 
                ["{:.1f}", "{:.1f}"], 
                ["{:.1f}", "{:.1f}"], 
                ["{:.1f}", "{:.1f}"], 
                ["{:.0f}", "{:.0f}"]]

    for i in range(len(annotations)):
        for j in range(len(annotations[0])):
            formatted_text = annotations[i][j].format(data_array[i][j])
            ax.text(j + 0.5, i + 0.5, formatted_text, 
                    ha='center', va='center', fontsize=10, color='white')
    
    return ax

def plot_match_statistics_table(ax, summary, player_stats, match_id):
    
    match_stats = create_match_stats(summary, player_stats, match_id)
    normalised_match_stats = get_normalised_match_stats(match_stats)
    
    ax = plot_heatmap(ax, normalised_match_stats)
    ax = annotate_heatmap(ax, match_stats)
    
    return ax