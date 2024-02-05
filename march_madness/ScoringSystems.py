import itertools

import networkx as nx
import pandas as pd

from Projects.ncaam.march_madness import Tournament as Bracket, TeamsInfo as Teams


# Take the team that has the better chance to win each matchup
def create_choice_df_better_head_to_head(chance_df):
    choice_df = chance_df.fillna(0).round()
    return choice_df


# Take the team that has the better chance to win the championship
def create_choice_df_overall_chance(chance_df, matchups_graph):
    total_chances = Bracket.calculate_game_chances(chance_df, matchups_graph)

    teams = chance_df.index
    choice_df = pd.DataFrame(columns=teams, index=teams)

    for team1, team2 in itertools.combinations(teams, 2):
        if team1 not in total_chances.index:
            team1_chance = 0
        else:
            team1_chance = total_chances.at[team1, 'Winner']
        if team2 not in total_chances.index:
            team2_chance = 0
        else:
            team2_chance = total_chances.at[team2, 'Winner']
        choice_df.at[team1, team2] = 1 if team2_chance > team1_chance else 0
        choice_df.at[team2, team1] = 1 if team1_chance > team2_chance else 0

    return choice_df


# Take the team that is expected to get the most points
def create_choice_df_most_points(chance_df, matchups_graph):
    total_chances = Bracket.calculate_game_chances(chance_df, matchups_graph)
    expected_points = Bracket.calculate_expected_points(total_chances)

    teams = chance_df.index
    choice_df = pd.DataFrame(columns=teams, index=teams)

    for team1, team2 in itertools.combinations(teams, 2):
        if team1 not in expected_points.index:
            team1_ep = 0
        else:
            team1_ep = expected_points.at[team1, 'Total']
        if team2 not in expected_points.index:
            team2_ep = 0
        else:
            team2_ep = expected_points.at[team2, 'Total']
        choice_df.at[team1, team2] = 1 if team2_ep > team1_ep else 0
        choice_df.at[team2, team1] = 1 if team1_ep > team2_ep else 0

    return choice_df


# Take the team that is expected to get the most points and eliminating teams that would have to play that team
def create_choice_df_most_points_eliminating(chance_df, matchups_graph):
    expected_points = Bracket.calculate_expected_points_eliminating(chance_df, matchups_graph)

    ordered_ranking = list(expected_points.index)
    choice_df = pd.DataFrame(columns=ordered_ranking, index=ordered_ranking)

    for team1, team2 in itertools.combinations(ordered_ranking, 2):
        team1_rank = ordered_ranking.index(team1)
        team2_rank = ordered_ranking.index(team2)
        choice_df.at[team1, team2] = 1 if team2_rank < team1_rank else 0
        choice_df.at[team2, team1] = 1 if team1_rank < team2_rank else 0

    return choice_df


# Take the team that is expected to get the most points in future games
def create_choice_df_most_points_greedy(chance_df, matchups_graph):
    expected_points = Bracket.calculate_expected_points_greedy(chance_df, matchups_graph)

    ordered_ranking = list(expected_points.index)
    choice_df = pd.DataFrame(columns=ordered_ranking, index=ordered_ranking)

    for team1, team2 in itertools.combinations(ordered_ranking, 2):
        team1_rank = ordered_ranking.index(team1)
        team2_rank = ordered_ranking.index(team2)
        choice_df.at[team1, team2] = 1 if team2_rank < team1_rank else 0
        choice_df.at[team2, team1] = 1 if team1_rank < team2_rank else 0

    return choice_df


def create_choice_df_most_points_best(chance_df, ranking_df, matchups_graph):
    expected_points = Bracket.calculate_expected_points_best(chance_df, ranking_df, matchups_graph)

    ordered_ranking = list(expected_points.index)
    choice_df = pd.DataFrame(columns=ordered_ranking, index=ordered_ranking)

    for team1, team2 in itertools.combinations(ordered_ranking, 2):
        team1_rank = ordered_ranking.index(team1)
        team2_rank = ordered_ranking.index(team2)
        choice_df.at[team1, team2] = 1 if team2_rank < team1_rank else 0
        choice_df.at[team2, team1] = 1 if team1_rank < team2_rank else 0

    return choice_df


# Sort the teams in a given set based on who would go furthest to least far according to the choices
def create_topology(team_df, choice_df):
    teams = team_df.index

    num_better = {team: sum(choice_df[team]) for team in teams}
    num_better = {team: count for team, count in sorted(num_better.items(), key=lambda t: t[1], reverse=True)}
    ordered_teams = list(num_better.keys())

    team_df = team_df.reindex(ordered_teams)
    return team_df


def completed_bracket(choice_df, matchups_graph):
    nodes = matchups_graph.nodes
    teams = {node for node in nodes if matchups_graph.in_degree(node) == 0}

    team_indexes = list(sorted(list(teams)))
    bracket_df = pd.DataFrame(columns=team_indexes, index=team_indexes)
    eliminated_teams = set()

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Play In',
                                                        4)

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Round of 32',
                                                        32)

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Sweet 16',
                                                        16)

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Elite 8',
                                                        8)

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Final 4',
                                                        4)

    remaining_teams = teams - eliminated_teams
    bracket_df, eliminated_teams = handle_bracket_round(remaining_teams,
                                                        choice_df,
                                                        matchups_graph,
                                                        bracket_df,
                                                        eliminated_teams,
                                                        'Championship',
                                                        2)

    remaining_teams = list(teams - eliminated_teams)
    team1 = remaining_teams[0]
    team2 = remaining_teams[1]

    team1_better = choice_df.at[team2, team1] == 1
    team2_better = choice_df.at[team1, team2] == 1

    if team1_better == team2_better:
        team1_better = True
        team2_better = False

    eliminated_team = team2 if team1_better else team1

    eliminated_teams.add(eliminated_team)

    bracket_df.at[team1, team2] = 1 if team2_better else -1
    bracket_df.at[team2, team1] = 1 if team1_better else -1

    bracket_df = bracket_df.fillna(0)
    return bracket_df


def handle_bracket_round(remaining_teams,
                         choice_df,
                         matchups_graph,
                         bracket_df,
                         eliminated_teams,
                         round_name,
                         teams_per_round):
    for play_in in [round_name + ' ' + str(num + 1) for num in range(teams_per_round)]:

        competing_teams = list()
        for team in remaining_teams:
            path = list(nx.all_simple_paths(matchups_graph, team, play_in))
            if path:
                competing_teams.append(team)

        if len(competing_teams) == 2:
            team1 = competing_teams[0]
            team2 = competing_teams[1]
        else:
            continue

        team1_better = choice_df.at[team2, team1] == 1
        team2_better = choice_df.at[team1, team2] == 1

        if team1_better == team2_better:
            team1_better = True
            team2_better = False

        eliminated_team = team2 if team1_better else team1

        eliminated_teams.add(eliminated_team)

        bracket_df.at[team1, team2] = 1 if team2_better else 0
        bracket_df.at[team2, team1] = 1 if team1_better else 0

    return bracket_df, eliminated_teams


def create_true_bracket_df(matchups_graph):
    nodes = matchups_graph.nodes
    teams = {node for node in nodes if matchups_graph.in_degree(node) == 0}

    name_mapping = Teams.map_schools_to_full_name()

    team_indexes = list(sorted(list(teams)))
    bracket_df = pd.DataFrame(columns=team_indexes, index=team_indexes)

    round_64_winners = []
    round_64_losers = []

    for winner, loser in zip(round_64_winners, round_64_losers):
        winner = name_mapping.get(winner, winner)
        loser = name_mapping.get(loser, loser)
        bracket_df.at[loser, winner] = 1
        bracket_df.at[winner, loser] = 0

    round_32_winners = []
    round_32_losers = []

    for winner, loser in zip(round_32_winners, round_32_losers):
        winner = name_mapping.get(winner, winner)
        loser = name_mapping.get(loser, loser)
        bracket_df.at[loser, winner] = 1
        bracket_df.at[winner, loser] = 0

    sweet_16_winners = []
    sweet_16_losers = []

    for winner, loser in zip(sweet_16_winners, sweet_16_losers):
        winner = name_mapping.get(winner, winner)
        loser = name_mapping.get(loser, loser)
        bracket_df.at[loser, winner] = 1
        bracket_df.at[winner, loser] = 0

    elite_8_winners = []
    elite_8_losers = []

    for winner, loser in zip(elite_8_winners, elite_8_losers):
        winner = name_mapping.get(winner, winner)
        loser = name_mapping.get(loser, loser)
        bracket_df.at[loser, winner] = 1
        bracket_df.at[winner, loser] = 0

    final_4_winners = []
    final_4_losers = []

    for winner, loser in zip(final_4_winners, final_4_losers):
        winner = name_mapping.get(winner, winner)
        loser = name_mapping.get(loser, loser)
        bracket_df.at[loser, winner] = 1
        bracket_df.at[winner, loser] = 0

    bracket_df = bracket_df.fillna(0)
    return bracket_df
