import datetime
import time

import pandas as pd
import requests

domain = 'https://api.natstat.com/v2/'
api_key = '87ab-ba0b1b'


def get(endpoint, params):
    req = requests.get(domain + endpoint, params=params)
    resp = req.json()
    return resp


def glossary():
    params = {'key': api_key,
              'format': 'json'}
    endpoint = 'glossary/MBB/'
    return get(endpoint, params=params)


def get_college_basketball_seasons():
    params = {'key': api_key,
              'format': 'json'}
    endpoint = 'seasons/MBB/'
    return get(endpoint, params=params)


def get_college_basketball_teams(season=2023):
    params = {'key': api_key,
              'format': 'json',
              'season': season,
              'max': 1000}
    endpoint = 'teams/MBB/'
    return get(endpoint, params=params)


def get_specific_college_basketball_teams(team_id):
    params = {'key': api_key,
              'format': 'json',
              'id': team_id}
    endpoint = 'teams/MBB/'
    return get(endpoint, params=params)


def get_games_for_team(team_id, start_date, end_date):
    params = {'key': api_key,
              'format': 'json',
              'start': start_date,
              'end': end_date,
              'team': team_id}
    endpoint = 'games/MBB/'
    return get(endpoint, params=params)


def get_boxscores_for_team(team_id, start_date, end_date):
    params = {'key': api_key,
              'format': 'json',
              'start': start_date,
              'end': end_date,
              'team': team_id}
    endpoint = 'boxscores/MBB/'
    return get(endpoint, params=params)


def get_stats_for_team(team_id, stat_code, season=2023):
    params = {'key': api_key,
              'format': 'json',
              'team': team_id,
              'stat': stat_code,
              'season': season}
    endpoint = 'stats/MBB/'
    return get(endpoint, params=params)


def get_season_games():
    start_date = datetime.date(2023, 11, 5)
    start_date = start_date.strftime('%Y-%m-%d')

    end_date = datetime.date.today() + datetime.timedelta(days=7)
    end_date = end_date.strftime('%Y-%m-%d')

    # teams = list()
    # for season in range(2007, 2023):
    #     cbb_teams = get_college_basketball_teams(season=season).get('teams')
    #     sdf = pd.DataFrame.from_dict(cbb_teams, orient='index')
    #     teams.append(sdf)
    # sdf = pd.concat(teams)
    # sdf = sdf.drop_duplicates()
    # for index, row in sdf.iterrows():
    #     team_id = row['ID']
    #     extra = get_specific_college_basketball_teams(team_id).get('teams').get('team_' + team_id)
    #     sdf.at[index, 'Nickname'] = extra.get('Nickname')
    #
    # sdf.to_csv('Projects/ncaam/march_madness/ncaamTeams.csv')

    cbb_teams = get_college_basketball_teams(season=2023).get('teams')
    cbb_teams = {k: v for k, v in cbb_teams.items() if v.get('Active') == 'Y'}

    current_api_calls = 0
    games = list()
    for team, team_dict in cbb_teams.items():
        current_api_calls = current_api_calls + 1
        team_id = team_dict.get('ID')
        if current_api_calls >= 2400:
            time.sleep(3600)
            current_api_calls = 0
        team_schedule = get_games_for_team(team_id, start_date, end_date).get('games')
        # team_schedule = get_boxscores_for_team(team_id, start_date, end_date).get('boxscores')
        team_schedule = {k: v for k, v in team_schedule.items()
                         if 'GameStatus' in v and v.get('GameStatus') == 'Final'}
        for game_id, game in team_schedule.items():
            if 'Neutral' in game:
                game['Neutral'] = 1 if game.get('Neutral') == 'Y' else 0
            if 'League' in game:
                del game['League']
            games.append(game)
    games_df = pd.DataFrame(games)

    games_df.to_csv('Projects/ncaam/march_madness/ncaamScores.csv', index=False)
    return games_df


def get_conferences():
    cbb_teams = get_college_basketball_teams(season=2023).get('teams')
    cbb_teams = {k: v for k, v in cbb_teams.items() if v.get('Active') == 'Y'}

    team_ids = [team.get('ID') for team in cbb_teams.values()]

    conf_mapping = dict()
    for team_id in team_ids:
        team = get_specific_college_basketball_teams(team_id)
        team = team.get('teams')
        team = [t for t in team.values() if t.get('ID') == team_id][0]
        name = team.get('Name')

        seasons = [season for season in team.get('seasons').values() if 'League' in season]
        valid_seasons = [int(season.get('ID')) for season in seasons]
        if valid_seasons:
            max_season = max(valid_seasons)
        else:
            continue
        latest_season = [season for season in seasons if int(season.get('ID')) == max_season][0]
        conference = latest_season.get('League')[0]

        conf_mapping[name] = conference

    conf_mapping = pd.Series(conf_mapping)
    conf_mapping.to_csv('Projects/ncaam/march_madness/ncaamConfs.csv')
    return conf_mapping
