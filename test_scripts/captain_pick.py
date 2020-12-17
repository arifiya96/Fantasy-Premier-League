import requests
import numpy as np 
import pandas as pd
import statistics

#These are the API URL's for each member in the team. Remember to update if I replace someone.
my_team_urls = ['https://fantasy.premierleague.com/api/element-summary/278/',
                  'https://fantasy.premierleague.com/api/element-summary/8/',
                  'https://fantasy.premierleague.com/api/element-summary/270/',
                  'https://fantasy.premierleague.com/api/element-summary/41/',
                  'https://fantasy.premierleague.com/api/element-summary/432/',
                  'https://fantasy.premierleague.com/api/element-summary/391/',
                  'https://fantasy.premierleague.com/api/element-summary/298/',
                  'https://fantasy.premierleague.com/api/element-summary/37/',
                  'https://fantasy.premierleague.com/api/element-summary/449/',
                  'https://fantasy.premierleague.com/api/element-summary/390/',
                  'https://fantasy.premierleague.com/api/element-summary/370/',
                  'https://fantasy.premierleague.com/api/element-summary/557/',
                  'https://fantasy.premierleague.com/api/element-summary/224/',
                  'https://fantasy.premierleague.com/api/element-summary/388/',
                  'https://fantasy.premierleague.com/api/element-summary/506/']

#Variable storage.
my_team_players = ['Ederson','Leno','Walker','Mings','Ogbonna','Dier','Maguire','Grealish','Soucek','Son','Ward-Prowse','Lookman','Vardy','Kane','Wilson']
my_team_fixtures = []
player_fixtures = {}

#Make the API call and store it in my_team_fixtures
def get_team_fixtures():
    for player in my_team_urls:
        #Convert to JSON
        player_json = requests.get(player).json()
        my_team_fixtures.append(player_json['fixtures'][0])

#Initialise the player fixtures dictionary
def initialise_player_fixtures():
    for player in my_team_players:
        player_fixtures[player] = []

#Put the fixtures difficulties in the player_fixture dictionary
def insert_fixtures():
    player_fixtures['Ederson'].append(my_team_fixtures[0]['difficulty'])
    player_fixtures['Ederson'].append(my_team_fixtures[0]['is_home'])
    player_fixtures['Leno'].append(my_team_fixtures[1]['difficulty'])
    player_fixtures['Leno'].append(my_team_fixtures[1]['is_home'])
    player_fixtures['Walker'].append(my_team_fixtures[2]['difficulty'])
    player_fixtures['Walker'].append(my_team_fixtures[2]['is_home'])
    player_fixtures['Mings'].append(my_team_fixtures[3]['difficulty'])
    player_fixtures['Mings'].append(my_team_fixtures[3]['is_home'])
    player_fixtures['Ogbonna'].append(my_team_fixtures[4]['difficulty'])
    player_fixtures['Ogbonna'].append(my_team_fixtures[4]['is_home'])
    player_fixtures['Dier'].append(my_team_fixtures[5]['difficulty'])
    player_fixtures['Dier'].append(my_team_fixtures[5]['is_home'])
    player_fixtures['Maguire'].append(my_team_fixtures[6]['difficulty'])
    player_fixtures['Maguire'].append(my_team_fixtures[6]['is_home'])
    player_fixtures['Grealish'].append(my_team_fixtures[7]['difficulty'])
    player_fixtures['Grealish'].append(my_team_fixtures[7]['is_home'])
    player_fixtures['Soucek'].append(my_team_fixtures[8]['difficulty'])
    player_fixtures['Soucek'].append(my_team_fixtures[8]['is_home'])
    player_fixtures['Son'].append(my_team_fixtures[9]['difficulty'])
    player_fixtures['Son'].append(my_team_fixtures[9]['is_home'])
    player_fixtures['Ward-Prowse'].append(my_team_fixtures[10]['difficulty'])
    player_fixtures['Ward-Prowse'].append(my_team_fixtures[10]['is_home'])
    player_fixtures['Lookman'].append(my_team_fixtures[11]['difficulty'])
    player_fixtures['Lookman'].append(my_team_fixtures[11]['is_home'])
    player_fixtures['Vardy'].append(my_team_fixtures[12]['difficulty'])
    player_fixtures['Vardy'].append(my_team_fixtures[12]['is_home'])
    player_fixtures['Kane'].append(my_team_fixtures[13]['difficulty'])
    player_fixtures['Kane'].append(my_team_fixtures[13]['is_home'])
    player_fixtures['Wilson'].append(my_team_fixtures[14]['difficulty'])
    player_fixtures['Wilson'].append(my_team_fixtures[14]['is_home'])

def display_captain_picker():
    df = pd.DataFrame(player_fixtures)
    df.index = ['Fixture Difficulty','Home']
    possible_captains = df.transpose()
    captain_picker = possible_captains[possible_captains.Home == True]
    print(captain_picker.sort_values(by=['Fixture Difficulty']))

#Fire all the functions
get_team_fixtures()
initialise_player_fixtures()
insert_fixtures()
display_captain_picker()