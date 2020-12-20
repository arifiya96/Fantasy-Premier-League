import streamlit as st 
import pandas as pd 
import numpy as np 
import statistics
import requests
import time

#Authentication
url = 'https://users.premierleague.com/accounts/login/'
session = requests.session()

#Title
st.image('premier_league.jpg')
st.title('Fantasy Premier League (Season 20-21)')
st.write('Load your team and decide your weekly lineups along with your captains.')

#Login credentials
st.write('Provide your fantasy premier league login and click load team. The load team button will only appear once you fill out all the fields.')
get_email_address = st.text_input('Email Address')
get_password = st.text_input('Password', type='password')
get_team_id = st.text_input('Team ID')
st.write('(You can find your team ID on the fantasy football website. When you log in, click on points and your ID will be in the URL. It looks something along the lines of fantasy.premierleague.com/entry/<your id>/event/13).')

#For API call
base_url = 'https://fantasy.premierleague.com/api/my-team/'
full_url = base_url + get_team_id + '/'
payload = {
        'password': get_password,
        'login': get_email_address,
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }

#When they click the button, do this
if get_email_address and get_password and get_team_id:
    if st.button('Load Team'):
        with st.spinner('Hold on... We are fetching your request. This may take a while.'):
            time.sleep(5)
            
        session.post(url, data=payload)
        data = session.get(full_url)

        my_team_ids = []
        def get_ids():
            data_json = data.json()
            picks = data_json['picks']
            for player in picks:
                my_team_ids.append(player['element'])
        
        team_data = []
        team_fixtures = []
        def get_player_points():
            base_url_1 = 'https://fantasy.premierleague.com/api/element-summary/'
            for player_id in my_team_ids:
                full_url_1 = base_url_1 + str(player_id) + '/'
                player_json = requests.get(full_url_1).json()
                team_data.append(player_json['history'])
                team_fixtures.append({
                    'ID': player_json['history'][0]['element'],
                    'Next_FDR': player_json['fixtures'][0]['difficulty'],
                    'Home': player_json['fixtures'][0]['is_home']
                })
        
        player_info = []
        def get_player_info():
            player_info_json = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
            player_info_element = player_info_json['elements']
            for player in player_info_element:
                player_info.append({
                    'Name': player['web_name'],
                    'ID': player['id']
                })
                for footballer in team_fixtures:
                    if footballer['ID'] == player['id']:
                        footballer['Name'] = player['web_name']
        
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
        
        def load_gameweek_scores():
            for player in team_data:
                for gw in player:
                    for my_player_id in player_scores:
                        if my_player_id['ID'] == gw['element']:
                            my_player_id['GW_Scores'].append(gw['total_points'])
        
        player_points = {}
        def forms_df():
            for player in player_scores:
                current_form = np.around(sum(player['GW_Scores'][-4:])/4, 2)
                current_consistency = np.around(statistics.stdev(player['GW_Scores'][-4:]), 2)
                season_form = np.around(sum(player['GW_Scores'])/len(player['GW_Scores']), 2)
                season_consistency = np.around(statistics.stdev(player['GW_Scores']), 2)
                player_points[player['Name']] = [current_form, current_consistency, season_form, season_consistency]
        
        def get_lowest_current_form():
            player_forms = pd.DataFrame(player_points)
            player_forms.index = ['Current Form','Current Consistency','Season Form','Season Consistency']
            st.title('My Team: Current Form and Season Form')
            st.write('The table below shows you the current form and the season form of all your players')
            st.markdown('**Current Form** = average scores from the last 4 gameweeks. The higher the form, the better.')
            st.markdown('**Current Consistency** = the level of consistency the player is performing from the last 4 games. A lower score means more consistentency. Is your player consistently good or consistently bad?')
            st.markdown('**Season Form** = same as current form but for all matches in the current season')
            st.markdown('**Season Consistency** = same as current consistency but for all matches in the current season')
            st.dataframe(player_forms.transpose().sort_values(by=['Current Form']))
        
        next_fixtures = {}
        def convert_to_dict():
            for player in team_fixtures:
                next_fixtures[player['Name']] = []
                next_fixtures[player['Name']].append(player['Next_FDR'])
                next_fixtures[player['Name']].append(player['Home'])
        
        def fixture_df():
            next_fixture_df = pd.DataFrame(next_fixtures)
            next_fixture_df.index = ['Fixture Difficulty','Home']
            st.title('My Team: Captain Choices')
            st.write('The table below shows you the fixture difficulty rating for the next game and whether this is a home fixture')
            st.markdown('**Fixture Difficulty Rating** = 1 is the easiest, 5 is the hardest')
            st.markdown('**Home** = whether they will be playing at home')
            st.write('Hopefully this gives you sufficient enough information to decide who will be your captain.')
            st.dataframe(next_fixture_df.transpose())
        
        def errors():
            if next_fixtures and player_points:
                st.success('Data Successfully Received')
            else:
                st.error('Something went wrong. Are you sure you inserted the correct credentials?')
        
        #run the functions
        get_ids()
        get_player_points()
        get_player_info()
        initialise_players()
        load_gameweek_scores()
        forms_df()
        get_lowest_current_form()
        convert_to_dict()
        fixture_df()
        errors()
    
    

    


    
    

