import requests
import pandas as pd 
import numpy as np 

#Get the authentication first before proceeding
url = 'https://users.premierleague.com/accounts/login/'
session = requests.session()
payload = {
    'password':'<STRING: Your Password>',
    'login':'<STRING: Your Email Address>',
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
def get_player_fixtures():
    base_url = 'https://fantasy.premierleague.com/api/element-summary/'
    for player_id in my_team_ids:
        full_url = base_url + str(player_id) + '/'
        player_json = requests.get(full_url).json()
        team_data.append({
            'ID': player_json['history'][0]['element'],
            'Next_FDR': player_json['fixtures'][0]['difficulty'],
            'Home': player_json['fixtures'][0]['is_home']
        })

#Get player names
def get_player_info():
    player_info_json = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
    player_info_element = player_info_json['elements']
    for player in player_info_element:
        for footballer in team_data:
            if footballer['ID'] == player['id']:
                footballer['Name'] = player['web_name']

#Put the fixtures into an dictionary for DF purposes
next_fixtures = {}
def convert_to_dict():
    for player in team_data:
        next_fixtures[player['Name']] = []
        next_fixtures[player['Name']].append(player['Next_FDR'])
        next_fixtures[player['Name']].append(player['Home'])

#Display the dataframe
def fixture_df():
    next_fixture_df = pd.DataFrame(next_fixtures)
    next_fixture_df.index = ['Fixture Difficulty','Home']
    possible_captains = next_fixture_df.transpose()
    captain_picker = possible_captains[possible_captains.Home == True]
    print(captain_picker.sort_values(by=['Fixture Difficulty']))

#Run the functions
get_ids()
get_player_fixtures()
get_player_info()
convert_to_dict()
fixture_df()