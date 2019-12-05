from __future__ import annotations

import argparse
import os
import pickle
import sys
from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from typing import List

import requests
from dateutil import parser as date_parser
# noinspection PyProtectedMember
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


TEAMS_URL = 'https://data.nba.net/prod/v2/2019/teams.json'
SIXERS_SCHEDULE_URL = 'https://data.nba.net/prod/v1/2019/teams/sixers/schedule.json'

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


def get_team_info():
    """
    Returns a mapping of nba.com team id -> team attributes, which look like this:

    {
        "isNBAFranchise": true,
        "isAllStar": false,
        "city": "Philadelphia",
        "altCityName": "Philadelphia",
        "fullName": "Philadelphia 76ers",
        "tricode": "PHI",
        "teamId": "1610612755",
        "nickname": "76ers",
        "urlName": "sixers",
        "teamShortName": "Philadelphia",
        "confName": "East",
        "divName": "Atlantic"
    }
    """
    resp = requests.get(TEAMS_URL)
    resp.raise_for_status()

    teams = resp.json()['league']['standard']
    team_info = {}
    for team in teams:
        if team['isNBAFranchise']:
            team_info[team['teamId']] = team

    return team_info


@dataclass
class Game:
    title: str
    start_time: datetime
    end_time: datetime


def get_schedule_data(only_upcoming: bool = False):
    team_info = get_team_info()
    current_time = datetime.now(timezone.utc)

    resp = requests.get(SIXERS_SCHEDULE_URL)
    resp.raise_for_status()

    data = resp.json()
    games = data['league']['standard']

    game_info = []
    for game in games:
        if game['seasonStageId'] != 2:
            continue

        away_team_name = team_info[game['vTeam']['teamId']]['nickname']
        home_team_name = team_info[game['hTeam']['teamId']]['nickname']

        title = f'{away_team_name} @ {home_team_name}'
        start_time = date_parser.parse(game['startTimeUTC'])
        end_time = start_time + timedelta(hours=2, minutes=30)

        if only_upcoming and end_time < current_time:
            continue

        game_info.append(Game(title, start_time, end_time))

    return game_info


def get_calendar_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('calendar', 'v3', credentials=credentials)

    return service


def get_calendar(service: Resource, calendar_name):
    if calendar_name == 'primary':
        # special case for just getting the primary calendar
        resp = service.calendarList().get(calendarId='primary').execute()
        return resp['id']

    resp = service.calendarList().list().execute()

    for calendar in resp['items']:
        if calendar['summary'] == calendar_name:
            return calendar['id']
    else:
        raise ValueError('Could not find calendar!')


class GameManager:
    update_nobody = 'none'

    def __init__(self, service: Resource, calendar_name):
        self.service = service
        self.calendar = get_calendar(service, calendar_name)

    def add_game(self, game: Game):
        body = {
            'summary': game.title,
            'start': {
                'dateTime': game.start_time.isoformat(),
            },
            'end': {
                'dateTime': game.end_time.isoformat(),
            },
            'colorId': 1
        }

        resp = self.service.events().insert(
            calendarId=self.calendar,
            body=body,
            sendUpdates=self.update_nobody,
        ).execute()

        return resp


def configure_calendar(calendar_name: str, games: List[Game]):
    """
    Configures a google calendar
    """
    manager = GameManager(get_calendar_service(), calendar_name)

    for idx, game in enumerate(games, start=1):
        manager.add_game(game)
        print(f'Added Game #{idx}: {game.title}')


def main():
    parser = argparse.ArgumentParser(description='Pull Sixers games into my Google calendar')
    parser.add_argument(
        '--calendar-name', default='primary',
        help='Name of the Calendar (summary in Calendar API) where events will get added'
    )
    parser.add_argument(
        '--all-games', action='store_true',
        help='Add all games for the 2019 season, not just future ones'
    )
    args = parser.parse_args()

    only_upcoming = not args.all_games
    games = get_schedule_data(only_upcoming=only_upcoming)

    configure_calendar(args.calendar_name, games)


if __name__ == '__main__':
    sys.exit(main())
