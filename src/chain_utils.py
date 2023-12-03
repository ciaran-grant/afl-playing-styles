import re

def get_venue_dimensions(chain_data, match_id):
    
    # Get match chain information
    match = chain_data[chain_data['Match_ID'] == match_id]

    return list(set(match['Venue_Width']))[0], list(set(match['Venue_Length']))[0]

def get_match(chain_data, match_id):
    
    return chain_data[chain_data['Match_ID'] == match_id]

def get_team(chain_data, team):
    
    return chain_data[chain_data['Team'] == team]

def get_player(chain_data, player):
    
    return chain_data[chain_data['Player'] == player]

def get_year(chain_data, year):
    
    return chain_data[chain_data['Year'] == year]

def add_space_before_capital_letters(string):
    return re.sub(r"\B([A-Z])", r" \1", string)

def get_teams(match_id):
    return add_space_before_capital_letters(match_id.split("_")[1]), add_space_before_capital_letters(match_id.split("_")[2])

def get_scores(summary):
    
    summary['Home_Goals'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[0].split(".")[0])
    summary['Home_Behinds'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[0].split(".")[1])
    summary['Home_Score'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[0].split(".")[2])
    
    summary['Away_Goals'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[1].split(".")[0])
    summary['Away_Behinds'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[1].split(".")[1])
    summary['Away_Score'] = summary['Q4_Score'].apply(lambda x: x.split(" - ")[1].split(".")[2])
    
    return summary
