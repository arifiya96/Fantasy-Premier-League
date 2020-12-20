# Fantasy-Premier-League
Data scripts to decide weekly player picks and captains

<b>team_info.py</b> is the main script used to load your team and get the following information for each player (requires authentication):
1) Current Form - calculated by getting the average points for the last 4 gameweeks
2) Current Consistency - calculated by getting the standard deviation of points for the last 4 game weeks
3) Season Form - calculated by getting the average points for the current season
4) Season Consistency - calculated by getting the standard deviation of points for the current season

<b>team_fixtures.py</b> is the main script to decide who should captain the next fixture. It will load the fixture difficulty rating for each player and whether they are playing home or not. The script will automatically filter away fixtures as the general consensus is to captain a home fixture. 

Web app active here:
https://fantasy-premier-league-squad.herokuapp.com/
