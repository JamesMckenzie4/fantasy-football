from bs4 import BeautifulSoup
import os
import requests
import re
import time


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
    base_url = 'https://www.oddschecker.com'
    matches_url = '/football/english/premier-league'

    full_markets_list = ['winner', 'first-goalscorer', 'both-teams-to-score', 'correct-score', 'half-time-full-time', 
                         'anytime-goalscorer', 'draw-no-bet', 'total-goals-over-under', 'total-goals-exact', 'asian-handicap',
                         'halftime', 'handicaps', 'last-goalscorer', 'match-result-and-both-teams-to-score', 'half-time-score',
                         'winning-margin', 'double-chance', 'team-to-score-first', 'to-win-to-nil', 'highest-scoring-half']
    # For now just get the following market data
    market_list = ['total-goals-over-under', 'winner', 'correct-score', 'asian-handicap', 'both-teams-to-score']

    # Get the page, make the soup
    page = requests.get(base_url + matches_url)
    soup = BeautifulSoup(page.content, 'lxml')

    # Iterate over all markets and all matches - populate csv files for each
    matches = soup.find("table", {"class": "at-hda standard-list"}).find_all('tr', {'class': 'match-on '})
    for market in market_list:
        # Need different table class name for over_under markets
        is_over_under = (market == 'total-goals-over-under')
        for match in matches:
            # Get team names
            team_1, team_2 = get_team_name(match)
            # Check data dir exists. If not, create one.
            if not os.path.isdir('../../data/odds-data/'):
                os.mkdir('../../data/odds-data/')
            with open('../../data/odds-data/{}_{}_{}.csv'.format(team_1, team_2, market), 'w') as write_file:
                # Get odds 
                href = match.find_all('td', {'class': 'betting link-right'})[0].a['href']
                href = '/'.join(href.split('/')[:-1])
                # Get odds html - wait 5 seconds to avoid a IP ban from oddschecker
                time.sleep(5)
                odds_page = requests.get('{}{}/{}'.format(base_url, href, market))
                odds_soup = BeautifulSoup(odds_page.content, 'lxml')
                # Get the main odds table
                odds_table = odds_soup.find('table', {'class': 'eventTable '})
                # Get the bookmakers names list        
                bookmakers = get_bookmakers(odds_table)
                # Get the odds dict
                selection_to_odds_map = get_odds_data(odds_table, is_over_under)
                write_file.write('Selection,{}\n'.format(','.join(bookmakers)))
                for selection, odds_data in selection_to_odds_map.items():
                    write_file.write('{},{}\n'.format(selection, ','.join(odds_data)))
                    
if __name__ == '__main__':
    main()