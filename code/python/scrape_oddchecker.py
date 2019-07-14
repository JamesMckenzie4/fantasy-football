from bs4 import BeautifulSoup
import os
import requests
import time

BASE_URL = 'https://www.oddschecker.com'
MATCHES_URL = '/football/english/premier-league'
MARKETS_LIST = ['winner', 'first-goalscorer', 'both-teams-to-score', 'correct-score', 'half-time-full-time',
                'anytime-goalscorer', 'draw-no-bet', 'total-goals-over-under', 'total-goals-exact', 'asian-handicap',
                'halftime', 'handicaps', 'last-goalscorer', 'match-result-and-both-teams-to-score', 'half-time-score',
                'winning-margin', 'double-chance', 'team-to-score-first', 'to-win-to-nil', 'highest-scoring-half']


def get_team_name(match):
    """Return the team names for the match in the order home_team, away_team"""
    teams = match.find_all('td', {'class': 'all-odds-click'})
    p_tags = teams[1].find_all('p')
    team_names = []
    for p_tag in p_tags:
        team_names.append(str(p_tag).split('beta-footnote">')[1].split('<')[0].replace(" ", "_"))
    return team_names[0], team_names[1]


def get_odds_data(odds_table, is_over_under):
    """Return a dictionary mapping the selection (e.g home_team, draw, away_team in match odds market) to a list
    of bookmakers odds"""
    selection_odds_map = {}
    if is_over_under:
        odds_table_rows = odds_table.find_all('tr', {'class': "diff-row handicap-participant evTabRow bc"})
    else:
        odds_table_rows = odds_table.find_all('tr', {'class': 'diff-row evTabRow bc'})
    for odds_table_row in odds_table_rows:
        team_name = odds_table_row['data-bname']
        decimal_odds = []
        for td in odds_table_row.find_all('td'):
            try:
                decimal_odds.append(td['data-odig'])
            except KeyError:
                continue
        selection_odds_map[team_name] = decimal_odds
    return selection_odds_map


def get_bookmakers(odds_table):
    bookmakers = []
    print(odds_table)
    table_headers = odds_table.find('tr', {'class': 'eventTableHeader'})
    for td in table_headers.find_all('td'):
        try:
            bookmakers.append(td.a['title'])
        except KeyError:
            continue
        except TypeError:
            continue
    return bookmakers


def main():
    # For now just get the following market data
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Get the page, make the soup
    page = requests.get(BASE_URL + MATCHES_URL, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    # Iterate over all markets and all matches - populate csv files for each
    matches = soup.find("table", {"class": "at-hda standard-list"}).find_all('tr')
    for match in matches:
        event_names = match.a
        if event_names:
            team_1, team_2 = event_names['data-event-name'].split(' v ')
        else:
            continue
        for market in ['total-goals-over-under', 'winner', 'correct-score', 'asian-handicap', 'both-teams-to-score']:
            # Check data dir exists. If not, create one.
            if not os.path.isdir('../../data/odds-data/'):
                os.mkdir('../../data/odds-data/')
            with open('../../data/odds-data/{}_{}_{}.csv'.format(team_1, team_2, market), 'w') as write_file:
                # Get odds
                href = match.find_all('td', {'class': 'betting link-right'})[0].a['href']
                # Get odds html - wait 5 seconds to avoid a IP ban from oddschecker
                time.sleep(1)
                print('{}{}/{}'.format(BASE_URL, href, market))
                """
                odds_page = requests.get('{}{}/{}'.format(BASE_URL, href, market), headers=headers)
                odds_soup = BeautifulSoup(odds_page.content, 'lxml')
                print(odds_soup)
                # Get the main odds table
                odds_table = odds_soup.find('table', {'class': 'eventTable '})
                # Get the bookmakers names list
                bookmakers = get_bookmakers(odds_table)
                # Get the odds dict
                selection_to_odds_map = get_odds_data(odds_table, is_over_under=(market == 'total-goals-over-under'))
                write_file.write('Selection,{}\n'.format(','.join(bookmakers)))
                for selection, odds_data in selection_to_odds_map.items():
                    write_file.write('{},{}\n'.format(selection, ','.join(odds_data)))"""


if __name__ == '__main__':
    main()