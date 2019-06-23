import argparse
import json
import os

from bs4 import BeautifulSoup
import requests


def pull_nba_players(store_location):
    """
    Creates a JSON file of whitelisted phrases for use in other programs.
    HTML pulled from Wikipedia

    :rtype: NoneType
    """
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_current_NBA_team_rosters')
    soup = BeautifulSoup(resp.content, 'html.parser')

    players = []
    coaches = []
    teams = []

    for player_element in soup.select('table > tbody > tr > td > table > tbody > tr > td:nth-child(3) > a'):
        # pull from title (first name last name format). strip if (basketball) disambiguation exists
        player_name = player_element.get('title').split('(')[0].lower()
        players.append(player_name)

    for coach_element in soup.select('table.toccolours > tbody > tr > td > ul:nth-child(2) > li:nth-child(1) > a'):
        coaches.append(coach_element.get('title').split('(')[0].lower())

    for team_element in soup.select('table.toccolours > tbody > tr > th:nth-child(1) > div:nth-child(1)'):
        team_full_name = team_element.text.split('roster')[0]
        teams.append(team_full_name)

    whitelist = {
        'whitelisted_phrases': [
            'league sources',
            'sources say',
            'trade',
            'pick',
            'camp',
            'cap space',
            'Sources',
        ],
        'blacklisted_urls': [
            'espn.com'
        ],
        'players': players,
        'coaches': coaches,
        'teams': teams,
    }
    with open(store_location, 'w') as f:
        f.write(json.dumps(whitelist, sort_keys=True, indent=2) + '\n')

    return


def main():
    parser = argparse.ArgumentParser(
        description='Pull NBA players list from Wikipedia page',
    )
    parser.add_argument(
        '--store',
        default=os.path.join(os.path.dirname(__file__), '..', 'secret', 'whitelist.json'),
        help='Where to store new whitelist file'
    )
    args = parser.parse_args()
    return pull_nba_players(args.store)


if __name__ == '__main__':
    main()
