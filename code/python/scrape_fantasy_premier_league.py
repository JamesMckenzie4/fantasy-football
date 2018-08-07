import requests
import time


def get_player_data():
    """Write player statistics to csv file"""
    all_info_url = 'https://fantasy.premierleague.com/drf/bootstrap'
    all_info = requests.get(all_info_url)
    all_info_json = all_info.json()
    player_info = all_info_json['elements']
    headers = list(player_info[0].keys())
    with open('../../data/fantasy-premier-league-data/players.csv', 'w') as write_file:
        write_file.write('{}\n'.format(','.join(headers)))
        for player in player_info:
            player_data = list(player.values())
            player_data = [str(i) for i in player_data]
            write_file.write('{}\n'.format(','.join(player_data)))
            
def get_player_fixtures(n_players=489):
    """Write player fixture list to csv file"""
    with open('../../data/fantasy-premier-league-data/player-fixtures.csv', 'w') as write_file:
        for i in range(1, n_players + 1):
            print('processing player - {}'.format(i))
            player_info_url = 'https://fantasy.premierleague.com/drf/element-summary/{}'.format(i)
            player_info = requests.get(player_info_url)
            fixtures = player_info.json()['fixtures']
            if i == 1:
                headers = list(fixtures[0].keys())
                write_file.write('{},{}\n'.format('player_id', ','.join(headers)))
            for fixture in fixtures:
                fixture_data = [str(i) for i in fixture.values()]
                write_file.write('{},{}\n'.format(i, ','.join(fixture_data)))
            time.sleep(1)
            
def get_player_types():
    """Get player type ID to position mapping"""
    with open('../../data/fantasy-premier-league-data/player-types.csv', 'w') as write_file:
        all_info_url = 'https://fantasy.premierleague.com/drf/bootstrap'
        all_info = requests.get(all_info_url)
        player_types = all_info.json()['element_types']
        headers = list(player_types[0].keys())
        write_file.write('{}\n'.format(','.join(headers)))
        for player_type in player_types:
            player_type = [str(i) for i in player_type.values()]
            write_file.write('{}\n'.format(','.join(player_type)))
            
def get_team_data():
    """Get team ID to name mapping as well as some team statistics"""
    with open('../../data/fantasy-premier-league-data/teams.csv', 'w') as write_file:
        all_info_url = 'https://fantasy.premierleague.com/drf/bootstrap'
        all_info = requests.get(all_info_url)
        teams = all_info.json()['teams']
        # Get rid of next fixture key
        for team in teams:
            team.pop('next_event_fixture')
        headers = list(teams[0].keys())
        write_file.write('{}\n'.format(','.join(headers)))
        for team in teams:
            team = [str(i) for i in team.values()]
            write_file.write('{}\n'.format(','.join(team)))
            
def main():
    get_player_data()
    get_player_fixtures()
    get_player_types()
    get_team_data()
    
if __name__ == "__main__":
    main()