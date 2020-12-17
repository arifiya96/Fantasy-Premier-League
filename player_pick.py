#USE team_info.py instead. The code here is messy and nested.

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

#Variable storage
team_data = []
player_scores = {}
player_points = {}

#Make the API call request and store it in team_data list
def get_data():
    for player in my_team_urls:
        #convert raw format to json
        player_json = requests.get(player).json()
        team_data.append(player_json['history'])

#Initialise each player with an empty list so I can append their scores later on
def initialise_player():
    for player in team_data:
        for data in player:
            if data['element'] == 278:
                player_scores['Ederson'] = []
                break
            elif data['element'] == 8:
                player_scores['Leno'] = []
                break
            elif data['element'] == 270:
                player_scores['Walker'] = []
                break
            elif data['element'] == 41:
                player_scores['Mings'] = []
                break
            elif data['element'] == 432:
                player_scores['Ogbonna'] = []
                break
            elif data['element'] == 391:
                player_scores['Dier'] = []
                break
            elif data['element'] == 298:
                player_scores['Maguire'] = []
                break
            elif data['element'] == 37:
                player_scores['Grealish'] = []
                break
            elif data['element'] == 449:
                player_scores['Soucek'] = []
                break
            elif data['element'] == 390:
                player_scores['Son'] = []
                break
            elif data['element'] == 370:
                player_scores['Ward-Prowse'] = []
                break
            elif data['element'] == 557:
                player_scores['Lookman'] = []
                break
            elif data['element'] == 224:
                player_scores['Vardy'] = []
                break
            elif data['element'] == 388:
                player_scores['Kane'] = []
                break
            elif data['element'] == 506:
                player_scores['Wilson'] = []
                break
            else:
                pass

#Put all their past gameweek points into player_scores dictionary
def store_points():
    for player in team_data:
        for data in player:
            if data['element'] == 278:
                player_scores['Ederson'].append(data['total_points'])
            elif data['element'] == 8:
                player_scores['Leno'].append(data['total_points'])
            elif data['element'] == 270:
                player_scores['Walker'].append(data['total_points'])
            elif data['element'] == 41:
                player_scores['Mings'].append(data['total_points'])
            elif data['element'] == 432:
                player_scores['Ogbonna'].append(data['total_points'])
            elif data['element'] == 391:
                player_scores['Dier'].append(data['total_points'])
            elif data['element'] == 298:
                player_scores['Maguire'].append(data['total_points'])
            elif data['element'] == 37:
                player_scores['Grealish'].append(data['total_points'])
            elif data['element'] == 449:
                player_scores['Soucek'].append(data['total_points'])
            elif data['element'] == 390:
                player_scores['Son'].append(data['total_points'])
            elif data['element'] == 370:
                player_scores['Ward-Prowse'].append(data['total_points'])
            elif data['element'] == 557:
                player_scores['Lookman'].append(data['total_points'])
            elif data['element'] == 224:
                player_scores['Vardy'].append(data['total_points'])
            elif data['element'] == 388:
                player_scores['Kane'].append(data['total_points'])
            elif data['element'] == 506:
                player_scores['Wilson'].append(data['total_points'])
            else:
                pass

#If you need to get the forms of a specific player
def get_season_form(player_name):
    season_form = np.round(sum(player_scores[player_name])/len(player_scores[player_name]), 2)
    season_consistency = np.round(statistics.stdev(player_scores[player_name]), 2)
    return season_form, season_consistency

def get_current_form(player_name):
    current_form = np.round(sum(player_scores[player_name][-4:])/4, 2)
    current_consistency = np.round(statistics.stdev(player_scores[player_name][-4:]), 2)
    return current_form, current_consistency

#Condense the points into form. Put into player_points list
def get_forms():
    for key, value in player_scores.items():
        current_form = np.round(sum(value[-4:])/4, 2)
        current_consistency = np.round(statistics.stdev(value[-4:]), 2)
        season_form = np.round(sum(value)/len(value), 2)
        season_consistency = np.round(statistics.stdev(value), 2)
        player_points[key] = [current_form, current_consistency, season_form, season_consistency]

#Initialise an object and update the current lowest form
def get_lowest_current_form():
    player_forms = pd.DataFrame(player_points)
    player_forms.index = ['Current Form','Current Consistency','Season Form','Season Consistency']
    print(player_forms.transpose().sort_values(by=['Current Form']))

#Execute the functions
get_data()
initialise_player()
store_points()
get_forms()
get_lowest_current_form()


