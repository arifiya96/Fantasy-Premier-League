import requests
import pandas as pd 
import numpy as np 
import statistics

#Get the authentication first before proceeding
url = 'https://users.premierleague.com/accounts/login/'
session = requests.session()
payload = {
    'password':'<String: your password>',
    'login':'<String: your email address>',
    'redirect_uri':'https://fantasy.premierleague.com/a/login',
    'app':'plfpl-web'
}
session.post(url, data=payload)
data = session.get('https://fantasy.premierleague.com/api/my-team/5261035/')

#Get the elements and store it in an empty list
my_team_ids = []
def get_ids():
    data_json = data.json()
    picks = data_json['picks']
    for player in picks:
        my_team_ids.append(player['element'])

#Using the team id's, append that to the URL to make the API call
team_data = []
def get_player_points():
    base_url = 'https://fantasy.premierleague.com/api/element-summary/'
    for player_id in my_team_ids:
        full_url = base_url + str(player_id) + '/'
        player_json = requests.get(full_url).json()
        team_data.append(player_json['history'])

#Get player names
player_info = []
def get_player_info():
    player_info_json = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
    player_info_element = player_info_json['elements']
    for player in player_info_element:
        player_info.append({
            'Name': player['web_name'],
            'ID': player['id']
        })

#Initialise player names in an empty dictionary
player_scores = []
def initialise_players():
    for my_player in my_team_ids:
        for player in player_info:
            if my_player == player['ID']:
                player_scores.append({
                    'Name': player['Name'],
                    'ID': player['ID'],
                    'GW_Scores': []
                })

#Put gameweek scores into player_scores list
def load_gameweek_scores():
    for player in team_data:
        for gw in player:
            for my_player_id in player_scores:
                if my_player_id['ID'] == gw['element']:
                    my_player_id['GW_Scores'].append(gw['total_points'])
            
#Convert the scores into a df and do the stats
player_points = {}
def forms_df():
    for player in player_scores:
        current_form = np.round(sum(player['GW_Scores'][-4:])/4, 2)
        current_consistency = np.round(statistics.stdev(player['GW_Scores'][-4:]), 2)
        season_form = np.round(sum(player['GW_Scores'])/len(player['GW_Scores']), 2)
        season_consistency = np.round(statistics.stdev(player['GW_Scores']), 2)
        player_points[player['Name']] = [current_form, current_consistency, season_form, season_consistency]

def get_lowest_current_form():
    player_forms = pd.DataFrame(player_points)
    player_forms.index = ['Current Form','Current Consistency','Season Form','Season Consistency']
    print(player_forms.transpose().sort_values(by=['Current Form']))

#run the functions
get_ids()
get_player_points()
get_player_info()
initialise_players()
load_gameweek_scores()
forms_df()
get_lowest_current_form()