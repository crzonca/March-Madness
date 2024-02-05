import math

import networkx as nx
import pandas as pd

from Projects.ncaam.march_madness import TeamRanking as Ranking
from Projects.ncaam.march_madness import TeamsInfo
from Projects.ncaam.march_madness import bracket as br


def get_play_in_teams(as_full_name=True):
    teams = [u for u, v in get_matchup_graph().edges if 'Play In' in v]
    if not as_full_name:
        schools_mapping = TeamsInfo.map_full_names_to_school()
        teams = [schools_mapping.get(team, team) for team in teams]
    return teams


def get_teams_by_seed(use_full_names=True):
    bracket = br.mm_bracket()
    teams = list(nx.topological_sort(bracket.to_graph()))[:bracket.size()]
    if not use_full_names:
        schools_mapping = TeamsInfo.map_full_names_to_school()
        teams = [schools_mapping.get(team, team) for team in teams]
    if len(set(teams)) != len(teams):
        duplicated_teams = [team for team in teams if teams.count(team) > 1]
        print('A team is duplicated', ' | '.join(duplicated_teams))
    return teams


def get_matchup_graph():
    bracket = br.mm_bracket()
    return bracket.to_graph()


def calculate_game_chances(chance_df, matchups_graph):
    teams = get_teams_by_seed()
    play_in_teams = get_play_in_teams()

    rounds = ['Round of 64', 'Round of 32', 'Sweet 16', 'Elite 8', 'Final 4', 'Championship', 'Winner']
    game_chances = pd.DataFrame(index=teams, columns=rounds)
    game_chances['Round of 64'] = 1.0

    game_chances.at[play_in_teams[0], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[0],
                                                                                       play_in_teams[1])
    game_chances.at[play_in_teams[1], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[1],
                                                                                       play_in_teams[0])

    # game_chances.at[play_in_teams[0], 'Round of 64'] = 1.0  # TAMU-CC
    # game_chances.at[play_in_teams[1], 'Round of 64'] = 0.0  # SE Missouri State

    game_chances.at[play_in_teams[2], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[2],
                                                                                       play_in_teams[3])
    game_chances.at[play_in_teams[3], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[3],
                                                                                       play_in_teams[2])

    # game_chances.at[play_in_teams[2], 'Round of 64'] = 0.0  # Texas Southern
    # game_chances.at[play_in_teams[3], 'Round of 64'] = 1.0  # FDU

    game_chances.at[play_in_teams[4], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[4],
                                                                                       play_in_teams[5])
    game_chances.at[play_in_teams[5], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[5],
                                                                                       play_in_teams[4])

    # game_chances.at[play_in_teams[4], 'Round of 64'] = 1.0  # Arizona State
    # game_chances.at[play_in_teams[5], 'Round of 64'] = 0.0  # Nevada

    game_chances.at[play_in_teams[6], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[6],
                                                                                       play_in_teams[7])
    game_chances.at[play_in_teams[7], 'Round of 64'] = Ranking.get_chance_to_beat_team(chance_df, play_in_teams[7],
                                                                                       play_in_teams[6])

    # game_chances.at[play_in_teams[6], 'Round of 64'] = 0.0  # Mississippi State
    # game_chances.at[play_in_teams[7], 'Round of 64'] = 1.0  # Pitt

    name_map = TeamsInfo.map_schools_to_full_name()

    # Round of 32
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 1)

    # TODO When a team wins manually set the values to 1 and 0
    # round_64_winners = ['Maryland', 'Furman', 'Missouri', 'Kansas', 'Alabama', 'San Diego State', 'Princeton',
    #                     'Houston', 'Auburn', 'Penn State', 'Duke', 'Tennessee', 'Northwestern', 'Arkansas',
    #                     'Texas', 'UCLA', 'Michigan State', "Saint Mary's", 'Xavier', 'Pitt', 'Creighton',
    #                     'Baylor', 'FDU', 'UConn', 'Gonzaga', 'Kentucky', 'Marquette', 'Miami', 'FAU',
    #                     'Kansas State', 'Indiana', 'TCU']
    # round_64_losers = ['West Virginia', 'Virginia', 'Utah State', 'Howard', 'TAMU-CC', 'Charleston', 'Arizona',
    #                    'Northern Kentucky', 'Iowa', 'TAMU', 'Oral Roberts', 'Louisiana', 'Boise State', 'Illinois',
    #                    'Colgate', 'UNC Asheville', 'USC', 'VCU', 'Kennesaw State', 'Iowa State', 'NC State',
    #                    'UCSB', 'Purdue', 'Iona', 'Grand Canyon', 'Providence', 'Vermont', 'Drake', 'Memphis',
    #                    'Montana State', 'Kent State', 'Arizona State']
    #
    # for winner, loser in zip(round_64_winners, round_64_losers):
    #     game_chances.at[name_map.get(winner), 'Round of 32'] = 1.0
    #     game_chances.at[name_map.get(loser), 'Round of 32'] = 0.0

    # Sweet 16
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 2)

    # round_32_winners = ['San Diego State', 'Tennessee', 'Arkansas', 'Princeton', 'Houston', 'Texas', 'UCLA',
    #                     'Alabama', 'Xavier', 'FAU', 'Kansas State', 'Michigan State', 'Miami', 'UConn',
    #                     'Creighton', 'Gonzaga']
    # round_32_losers = ['Furman', 'Duke', 'Kansas', 'Missouri', 'Auburn', 'Penn State', 'Northwestern',
    #                    'Maryland', 'Pitt', 'FDU', 'Kentucky', 'Marquette', 'Indiana', "Saint Mary's",
    #                    'Baylor', 'TCU']
    #
    # for winner, loser in zip(round_32_winners, round_32_losers):
    #     game_chances.at[name_map.get(winner), 'Sweet 16'] = 1.0
    #     game_chances.at[name_map.get(loser), 'Sweet 16'] = 0.0

    # Elite 8
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 3)

    # sweet_16_winners = ['Gonzaga', 'UConn', 'Kansas State', 'FAU', 'San Diego State', 'Miami', 'Creighton', 'Texas']
    # sweet_16_losers = ['UCLA', 'Arkansas', 'Michigan State', 'Tennessee', 'Alabama', 'Houston', 'Princeton', 'Xavier']
    #
    # for winner, loser in zip(sweet_16_winners, sweet_16_losers):
    #     game_chances.at[name_map.get(winner), 'Elite 8'] = 1.0
    #     game_chances.at[name_map.get(loser), 'Elite 8'] = 0.0

    # Final 4
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 4)

    # elite_8_winners = ['FAU', 'UConn', 'San Diego State', 'Miami']
    # elite_8_losers = ['Kansas State', 'Gonzaga', 'Creighton', 'Texas']
    #
    # for winner, loser in zip(elite_8_winners, elite_8_losers):
    #     game_chances.at[name_map.get(winner), 'Final 4'] = 1.0
    #     game_chances.at[name_map.get(loser), 'Final 4'] = 0.0

    # Championship
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 5)

    # final_4_winners = ['San Diego State', 'UConn']
    # final_4_losers = ['FAU', 'Miami']
    #
    # for winner, loser in zip(final_4_winners, final_4_losers):
    #     game_chances.at[name_map.get(winner), 'Championship'] = 1.0
    #     game_chances.at[name_map.get(loser), 'Championship'] = 0.0

    # Winner
    game_chances = calculate_round_chances(game_chances, chance_df, matchups_graph, teams, 6)

    if abs(sum(game_chances['Round of 64']) - 64) > 1e-8:
        print('Incorrect calculation at the round of 64')
    if abs(sum(game_chances['Round of 32']) - 32) > 1e-8:
        print('Incorrect calculation at the round of 32')
    if abs(sum(game_chances['Sweet 16']) - 16) > 1e-8:
        print('Incorrect calculation at the sweet 16')
    if abs(sum(game_chances['Elite 8']) - 8) > 1e-8:
        print('Incorrect calculation at the elite 8')
    if abs(sum(game_chances['Final 4']) - 4) > 1e-8:
        print('Incorrect calculation at the final 4')
    if abs(sum(game_chances['Championship']) - 2) > 1e-8:
        print('Incorrect calculation at the championship')
    if abs(sum(game_chances['Winner']) - 1) > 1e-8:
        print('Incorrect calculation for the winner')
    # game_chances = game_chances.sort_values(by='Winner', kind='mergesort', ascending=False)
    game_chances = game_chances.sort_values(by=['Winner',
                                                'Championship',
                                                'Final 4',
                                                'Elite 8',
                                                'Sweet 16',
                                                'Round of 32',
                                                'Round of 64'], kind='mergesort', ascending=[False,
                                                                                             False,
                                                                                             False,
                                                                                             False,
                                                                                             False,
                                                                                             False,
                                                                                             False])
    return game_chances


def calculate_round_chances(df, chance_df, matchup_graph, teams, round_num):
    col_names = {1: 'Round of 64',
                 2: 'Round of 32',
                 3: 'Sweet 16',
                 4: 'Elite 8',
                 5: 'Final 4',
                 6: 'Championship',
                 7: 'Winner'}

    for team in teams:
        team_chance_to_make_game = df.at[team, col_names.get(round_num)]

        victory_chances = list()
        possible_opponents = get_possible_opponents(matchup_graph, team, round_num)
        for possible_opponent in possible_opponents:
            opponent_chance_to_make_game = df.at[possible_opponent, col_names.get(round_num)]
            team_chance_to_beat_opponent = Ranking.get_chance_to_beat_team(chance_df, team, possible_opponent)
            victory_chances.append(opponent_chance_to_make_game * team_chance_to_beat_opponent)

        team_chance = team_chance_to_make_game * sum(victory_chances)
        try:
            df.at[team, col_names.get(round_num + 1)] = team_chance
        except ValueError as e:
            print(team, 'is missing or duplicated')
            raise e

    return df


def get_possible_opponents(graph, team, games_played):
    play_in_teams = get_play_in_teams()

    path = list(nx.all_simple_paths(graph, team, 'Winner'))[0]
    team_game = path[games_played + 1] if team in play_in_teams else path[games_played]
    path = path[1:games_played + 1] if team in play_in_teams else path[:games_played]

    all_opponents = {node for node in graph.nodes if graph.in_degree(node) == 0}

    teams_that_play_in_same_game = set()
    for possible_opponent in all_opponents:
        opponent_games_played = games_played + 1 if possible_opponent in play_in_teams else games_played
        opponent_path = list(nx.all_simple_paths(graph, possible_opponent, 'Winner'))[0]
        if opponent_path[opponent_games_played] == team_game:
            teams_that_play_in_same_game.add(possible_opponent)

    teams_that_meet_earlier = set()
    for possible_opponent in teams_that_play_in_same_game:
        opponent_games_played = games_played + 1 if possible_opponent in play_in_teams else games_played
        opponent_path = list(nx.all_simple_paths(graph, possible_opponent, 'Winner'))[0]
        opponent_path = opponent_path[1:opponent_games_played] if possible_opponent in play_in_teams \
            else opponent_path[:opponent_games_played]
        for game, opponent_game in zip(path, opponent_path):
            if game == opponent_game:
                teams_that_meet_earlier.add(possible_opponent)

    possible_opponents = teams_that_play_in_same_game - teams_that_meet_earlier

    return possible_opponents


def calculate_expected_points(game_chances):
    march_madness_points_df = game_chances.copy()
    march_madness_points_df['Round of 32'] = march_madness_points_df['Round of 32'] * 10
    march_madness_points_df['Sweet 16'] = march_madness_points_df['Sweet 16'] * 20
    march_madness_points_df['Elite 8'] = march_madness_points_df['Elite 8'] * 40
    march_madness_points_df['Final 4'] = march_madness_points_df['Final 4'] * 80
    march_madness_points_df['Championship'] = march_madness_points_df['Championship'] * 160
    march_madness_points_df['Winner'] = march_madness_points_df['Winner'] * 320
    march_madness_points_df = march_madness_points_df.drop(columns=['Round of 64'])
    march_madness_points_df['Total'] = march_madness_points_df.apply(lambda r: r['Round of 32'] +
                                                                               r['Sweet 16'] +
                                                                               r['Elite 8'] +
                                                                               r['Final 4'] +
                                                                               r['Championship'] +
                                                                               r['Winner'], axis=1)
    march_madness_points_df = march_madness_points_df.sort_values(by='Total', kind='mergesort', ascending=False)
    return march_madness_points_df


def calculate_expected_points_eliminating(chance_df, matchups_graph):
    total_chances = calculate_game_chances(chance_df, matchups_graph)
    expected_points = calculate_expected_points(total_chances)

    all_teams = {node for node in matchups_graph.nodes if matchups_graph.in_degree(node) == 0}
    play_in_teams = get_play_in_teams()
    chosen_teams = set()

    col_names = {0: 'Round of 64',
                 1: 'Round of 32',
                 2: 'Sweet 16',
                 3: 'Elite 8',
                 4: 'Final 4',
                 5: 'Championship',
                 6: 'Winner'}

    unchosen_teams = all_teams - chosen_teams
    while len(chosen_teams) < 32:
        unchosen_team_df = expected_points.loc[list(unchosen_teams)]
        unchosen_team_df = unchosen_team_df.sort_values(by='Total', kind='mergesort', ascending=False)

        # Get the team expected to get the most points throughout the tournament
        best_team = unchosen_team_df['Total'].index[0]

        # Determine which teams they would possibly have to play to get through the tournament
        best_path = list(nx.all_simple_paths(matchups_graph, best_team, 'Winner'))[0]
        chosen_teams.add(best_team)

        unchosen_teams = all_teams - chosen_teams

        # For each team that isnt going further than them
        for team in unchosen_teams:

            # Determine which teams they would possibly have to play to get through the tournament
            team_path = list(nx.all_simple_paths(matchups_graph, team, 'Winner'))[0]

            # If that less viable team would have to play the team
            #   Since we wouldn't pick the less viable team, set their expected points to 0
            if team in play_in_teams:
                team_path = team_path[1:]
            for index, games in enumerate(zip(best_path, team_path)):
                game1, game2 = games
                if game1 == game2:
                    expected_points.at[team, col_names.get(index)] = 0.0

        # Recalculate each teams total expected points to determine what the next most viable team is
        expected_points['Total'] = expected_points.apply(lambda r: r['Round of 32'] +
                                                                   r['Sweet 16'] +
                                                                   r['Elite 8'] +
                                                                   r['Final 4'] +
                                                                   r['Championship'] +
                                                                   r['Winner'], axis=1)

    expected_points = expected_points.sort_values(by=['Winner',
                                                      'Championship',
                                                      'Final 4',
                                                      'Elite 8',
                                                      'Sweet 16',
                                                      'Round of 32',
                                                      'Total'], kind='mergesort', ascending=False)

    return expected_points


def calculate_expected_points_greedy(chance_df, matchups_graph):
    total_chances = calculate_game_chances(chance_df, matchups_graph)
    expected_points = calculate_expected_points(total_chances)

    all_teams = {node for node in matchups_graph.nodes if matchups_graph.in_degree(node) == 0}
    col_names = {0: 'Round of 64',
                 1: 'Round of 32',
                 2: 'Sweet 16',
                 3: 'Elite 8',
                 4: 'Final 4',
                 5: 'Championship',
                 6: 'Winner'}

    for round_index in range(1, 7):
        expected_points = handle_round_greedy(expected_points, matchups_graph, col_names, all_teams, round_index)

    expected_points['Total'] = expected_points.apply(lambda r: r['Round of 32'] +
                                                               r['Sweet 16'] +
                                                               r['Elite 8'] +
                                                               r['Final 4'] +
                                                               r['Championship'] +
                                                               r['Winner'], axis=1)

    expected_points = expected_points.sort_values(by=['Winner',
                                                      'Championship',
                                                      'Final 4',
                                                      'Elite 8',
                                                      'Sweet 16',
                                                      'Round of 32',
                                                      'Total'], kind='mergesort', ascending=False)

    return expected_points


def calculate_expected_points_best(chance_df, ranking_df, matchups_graph):
    total_chances = calculate_game_chances(chance_df, matchups_graph)
    expected_points = calculate_expected_points(total_chances)

    all_teams = {node for node in matchups_graph.nodes if matchups_graph.in_degree(node) == 0}
    col_names = {0: 'Round of 64',
                 1: 'Round of 32',
                 2: 'Sweet 16',
                 3: 'Elite 8',
                 4: 'Final 4',
                 5: 'Championship',
                 6: 'Winner'}

    for round_index in range(1, 7):
        expected_points = handle_round_best(ranking_df,
                                            expected_points,
                                            matchups_graph,
                                            col_names,
                                            all_teams,
                                            round_index)

    expected_points['Total'] = expected_points.apply(lambda r: r['Round of 32'] +
                                                               r['Sweet 16'] +
                                                               r['Elite 8'] +
                                                               r['Final 4'] +
                                                               r['Championship'] +
                                                               r['Winner'], axis=1)

    expected_points = expected_points.sort_values(by=['Winner',
                                                      'Championship',
                                                      'Final 4',
                                                      'Elite 8',
                                                      'Sweet 16',
                                                      'Round of 32',
                                                      'Total'], kind='mergesort', ascending=False)

    return expected_points


def handle_round_greedy(expected_points, matchups_graph, col_names, remaining_teams, round_index):
    num_round_winners = int(math.pow(2, 6 - round_index))

    if round_index == 6:
        games = [col_names.get(round_index)]
    else:
        games = [col_names.get(round_index) + ' ' + str(n + 1) for n in range(num_round_winners)]

    # For each game in the round
    for game in games:
        team_losses = dict()

        # For each team
        for team in remaining_teams:
            paths_to_game = list(nx.all_simple_paths(matchups_graph, team, game))

            # See how many points we lose out on if we don't select that team
            if paths_to_game:
                potential_loss = sum(expected_points.loc[team][round_index - 1:-1])
                team_losses[team] = potential_loss
            else:
                continue

        # For each team that doesnt cost us the most
        team_losses = {team: loss for team, loss in sorted(team_losses.items(), key=lambda t: t[1], reverse=True)}
        for losing_team in list(team_losses.keys())[1:]:

            # Determine the team is no longer viable and set all future possible points to 0
            for col_index, col_name in list(col_names.items())[round_index:]:
                expected_points.at[losing_team, col_name] = 0.0

    return expected_points


def handle_round_best(ranking_df, expected_points, matchups_graph, col_names, remaining_teams, round_index):
    num_round_winners = int(math.pow(2, 6 - round_index))

    if round_index == 6:
        games = [col_names.get(round_index)]
    else:
        games = [col_names.get(round_index) + ' ' + str(n + 1) for n in range(num_round_winners)]

    # For each game in the round
    for game in games:
        team_losses = dict()

        # For each team
        for team in remaining_teams:
            paths_to_game = list(nx.all_simple_paths(matchups_graph, team, game))

            # See how many points we lose out on if we don't select that team
            if paths_to_game:
                if 'BT' in ranking_df.columns:
                    potential_loss = ranking_df.at[team, 'BT']
                else:
                    school_mapping = TeamsInfo.map_full_names_to_school()
                    school = school_mapping.get(team, team)
                    potential_loss = ranking_df.at[school, 'Coef Score']
                team_losses[team] = potential_loss
            else:
                continue

        # For each team that doesnt cost us the most
        team_losses = {team: loss for team, loss in sorted(team_losses.items(), key=lambda t: t[1], reverse=True)}
        for losing_team in list(team_losses.keys())[1:]:

            # Determine the team is no longer viable and set all future possible points to 0
            for col_index, col_name in list(col_names.items())[round_index:]:
                expected_points.at[losing_team, col_name] = 0.0

    return expected_points