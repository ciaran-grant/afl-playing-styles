import matplotlib.pyplot as plt
from visualisation.afl_colours import team_colourmaps
from chain_utils import get_match, get_team
from visualisation.plotting_pitches import plot_half_vertical_pitch_ax

def create_set_shot_indicator(chain_data):
    
    chain_data['Set_Shot'] = chain_data['Event_Type1'].apply(lambda x: ("Mark" in str(x)) or ("Free" in str(x)))
    
    return chain_data

def get_shots(chain_data):
    
    shots = chain_data[chain_data['Shot_At_Goal'] == True]
    
    return shots

def get_set_shots(chain_data):
    
    shots = chain_data[chain_data['Shot_At_Goal'] == True]
    set_shots = shots[shots['Set_Shot'] == True]
    
    return set_shots

def get_open_shots(chain_data):
    
    shots = chain_data[chain_data['Shot_At_Goal'] == True]
    open_shots = shots[shots['Set_Shot'] == False]
    
    return open_shots

def get_shot_outcome(shots, final_state):
    
    return shots[shots['Final_State'] == final_state]

def get_shot_data_dict(chains, match_id, team):
    
    chains = create_set_shot_indicator(chains)
    match_chains = get_match(chains, match_id=match_id)
    team_chains = get_team(match_chains, team=team)
    set_shots = get_set_shots(team_chains)
    open_shots = get_open_shots(team_chains)
    
    shot_data_dict = {
        'set_goals': get_shot_outcome(set_shots, "goal"),
        'set_behinds': get_shot_outcome(set_shots, "behind"),
        'set_misses':get_shot_outcome(set_shots, "miss"),
        'open_goals': get_shot_outcome(open_shots, "goal"),
        'open_behinds': get_shot_outcome(open_shots, "behind"),
        'open_misses': get_shot_outcome(open_shots, "miss")}
    
    return shot_data_dict

def plot_expected_score_map(pitch, ax, shot_data_dict, cmap, size_ratio = 3):

    norm = plt.Normalize(vmin=0, vmax=6)
    
    pitch.scatter(shot_data_dict['set_misses']['x'], shot_data_dict['set_misses']['y'], ax=ax, s=(shot_data_dict['set_misses']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['set_misses']['xScore'])), alpha=0.3, marker="s")
    pitch.scatter(shot_data_dict['set_behinds']['x'], shot_data_dict['set_behinds']['y'], ax=ax, s=(shot_data_dict['set_behinds']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['set_behinds']['xScore'])), marker="s")
    pitch.scatter(shot_data_dict['set_goals']['x'], shot_data_dict['set_goals']['y'], ax=ax, s=(shot_data_dict['set_goals']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['set_goals']['xScore'])), ec="white", marker="s")

    pitch.scatter(shot_data_dict['open_misses']['x'], shot_data_dict['open_misses']['y'], ax=ax, s=(shot_data_dict['open_misses']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['open_misses']['xScore'])), alpha=0.3)
    pitch.scatter(shot_data_dict['open_behinds']['x'], shot_data_dict['open_behinds']['y'], ax=ax, s=(shot_data_dict['open_behinds']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['open_behinds']['xScore'])))
    pitch.scatter(shot_data_dict['open_goals']['x'], shot_data_dict['open_goals']['y'], ax=ax, s=(shot_data_dict['open_goals']['xScore']**2)*size_ratio, c=cmap(norm(shot_data_dict['open_goals']['xScore'])), ec="white")
    
    return pitch, ax

def add_vertical_shot_map_legend(fig, ax, cmap, size_ratio = 3):
    
    norm = plt.Normalize(vmin=0, vmax=6)
    
    ## Manual Legend
    legend_ax = fig.add_axes([0.72, 0.4, 0.2, 0.3])
    legend_ax.axis("off")
    plt.xlim([0, 7.1])
    plt.ylim([0, 1.1])
    legend_ax.xaxis.set_tick_params(color="white")
    for size in [1, 2, 3, 4, 5, 6]:
        legend_ax.scatter(size, 0.95, s=(size**2)*size_ratio, c=cmap(norm(size)))
    for size in [1, 6]:
        legend_ax.text(size-0.14, 0.82, str(size), color="white", fontsize=8, font='Karla')
        
    legend_ax.scatter(3.5, 0.65, s=(4**2)*size_ratio, c=cmap(norm(4)), ec="white")
    legend_ax.scatter(3.5, 0.53, s=(4**2)*size_ratio, c=cmap(norm(4)))
    legend_ax.scatter(3.5, 0.41, s=(4**2)*size_ratio, c=cmap(norm(4)), alpha=0.3)
    legend_ax.scatter(5, 0.65, s=(4**2)*size_ratio, c=cmap(norm(4)), ec="white", marker="s")
    legend_ax.scatter(5, 0.53, s=(4**2)*size_ratio, c=cmap(norm(4)), marker = "s")
    legend_ax.scatter(5, 0.41, s=(4**2)*size_ratio, c=cmap(norm(4)), alpha=0.3, marker = "s")

    legend_ax.text(2.8, 0.73, "Open", color="white", fontsize=8, font='Karla')
    legend_ax.text(4.5, 0.73, "Set", color="white", fontsize=8, font='Karla')
    legend_ax.text(1, 0.62, "Goal", color="white", fontsize=8, font='Karla')
    legend_ax.text(1, 0.5, "Behind", color="white", fontsize=8, font='Karla')
    legend_ax.text(1, 0.38, "Miss", color="white", fontsize=8, font='Karla')
    
    return ax

def plot_vertical_pitch_team_expected_score(ax, chain_data, match_id, team):
    
    shot_data_dict = get_shot_data_dict(chain_data, match_id, team)
    pitch, ax = plot_half_vertical_pitch_ax(ax)
    pitch, ax = plot_expected_score_map(pitch, ax, shot_data_dict, cmap = team_colourmaps[team], size_ratio = 3)
    
    return ax