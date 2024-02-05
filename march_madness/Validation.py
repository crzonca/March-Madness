import pandas as pd

from Projects.ncaam.march_madness import TeamSeason as Season, Tournament as Bracket


def validate_team(team):
    graph = Season.get_games_graph()
    graph = Season.update_graph(graph)

    home_winner_graph, neut_winner_graph, away_winner_graph = Season.get_location_games_graph()
    neut_winner_graph = Season.update_graph(neut_winner_graph)

    wins = graph.in_degree(team)
    losses = graph.out_degree(team)
    teams_defeated = [opponent for opponent, team in list(graph.in_edges(team))]
    teams_lost_to = [opponent for team, opponent in list(graph.out_edges(team))]
    print_validation(wins, losses, teams_defeated, teams_lost_to, record_type='Overall')

    home_wins = home_winner_graph.in_degree(team)
    home_losses = away_winner_graph.out_degree(team)
    home_teams_defeated = [opponent for opponent, team in list(home_winner_graph.in_edges(team))]
    home_teams_lost_to = [opponent for team, opponent in list(away_winner_graph.out_edges(team))]
    print_validation(home_wins, home_losses, home_teams_defeated, home_teams_lost_to,
                     record_type='Home', location='at Home:')

    neutral_wins = neut_winner_graph.in_degree(team)
    neutral_losses = neut_winner_graph.out_degree(team)
    neutral_teams_defeated = [opponent for opponent, team in list(neut_winner_graph.in_edges(team))]
    neutral_teams_lost_to = [opponent for team, opponent in list(neut_winner_graph.out_edges(team))]
    print_validation(neutral_wins, neutral_losses, neutral_teams_defeated, neutral_teams_lost_to,
                     record_type='Neutral Site', location='at a Neutral Site:')

    away_wins = away_winner_graph.in_degree(team)
    away_losses = home_winner_graph.out_degree(team)
    away_teams_defeated = [opponent for opponent, team in list(away_winner_graph.in_edges(team))]
    away_teams_lost_to = [opponent for team, opponent in list(home_winner_graph.out_edges(team))]
    print_validation(away_wins, away_losses, away_teams_defeated, away_teams_lost_to,
                     record_type='Road', location='on the Road:')

    games_df = pd.read_csv('Projects/ncaam/march_madness/ncaamScores.csv')
    games_df = games_df.loc[(games_df['Visitor'] == team) | (games_df['Home'] == team)]
    games_df = games_df.drop_duplicates(subset=['ID', 'Visitor', 'Visitor_ID', 'Home', 'Home_ID'])
    games_df = games_df.drop(columns=['Visitor_ID', 'Home_ID', 'Winner_ID', 'Loser_ID'])
    games_df['GameDay'] = pd.to_datetime(games_df['GameDay'])
    games_df = games_df.sort_values(by='GameDay')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(games_df.reset_index(drop=True))


def print_validation(wins, losses, teams_defeated, teams_lost_to, record_type='', location=':'):
    justify_width = 35

    print(record_type, 'Record:', str(wins) + ' - ' + str(losses))

    teams_defeated_count = {team: teams_defeated.count(team) for team in teams_defeated}
    print('Teams Defeated', location)
    for team, count in sorted(teams_defeated_count.items(), key=lambda t: t[0]):
        count_str = 'x' + str(count) if count > 1 else ''
        print('\t' + team.ljust(justify_width) + count_str)

    teams_lost_to_count = {team: teams_lost_to.count(team) for team in teams_lost_to}
    print('Teams Lost To', location)
    for team, count in sorted(teams_lost_to_count.items(), key=lambda t: t[0]):
        count_str = 'x' + str(count) if count > 1 else ''
        print('\t' + team.ljust(justify_width) + count_str)
    print()


def get_possible_missing(bt_df, games_graph):
    teams = Bracket.get_teams_by_seed()
    bt_df = bt_df.loc[teams]
    school_mapping = Bracket.map_full_names_to_school()

    true_records = {'Kennesaw State': (26, 8),
                    'Liberty': (26, 8),
                    'Eastern Kentucky': (20, 13),
                    'Houston': (31, 3),
                    'Memphis': (26, 8),
                    'VCU': (27, 7),
                    'Miami': (25, 7),
                    'Virginia': (25, 7),
                    'Clemson': (23, 10),
                    'Duke': (26, 8),
                    'Pitt': (22, 11),
                    'NC State': (23, 10),
                    'Kansas': (27, 7),
                    'Texas': (26, 8),
                    'Kansas State': (23, 9),
                    'Baylor': (22, 10),
                    'Iowa State': (19, 13),
                    'TCU': (21, 12),
                    'West Virginia': (19, 14),
                    'Marquette': (28, 6),
                    'Xavier': (25, 9),
                    'Creighton': (21, 12),
                    'UConn': (25, 8),
                    'Providence': (21, 11),
                    'Vermont': (23, 10),
                    'Eastern Washington': (22, 10),
                    'Montana State': (25, 9),
                    'UNC Asheville': (27, 7),
                    'Longwood': (20, 12),
                    'Purdue': (29, 5),
                    'Northwestern': (21, 11),
                    'Indiana': (22, 11),
                    'Michigan State': (19, 12),
                    'Iowa': (19, 13),
                    'Maryland': (21, 12),
                    'Illinois': (20, 12),
                    'UCSB': (27, 7),
                    'Hofstra': (24, 9),
                    'Charleston': (31, 3),
                    'FAU': (31, 3),
                    'Northern Kentucky': (22, 12),
                    'Princeton': (21, 8),
                    'Yale': (21, 8),
                    'Iona': (27, 7),
                    'Toledo': (27, 7),
                    'Kent State': (28, 6),
                    'Howard': (22, 12),
                    'Drake': (27, 7),
                    'San Diego State': (27, 6),
                    'Utah State': (26, 8),
                    'Boise State': (24, 9),
                    'Nevada': (22, 10),
                    'FDU': (19, 15),
                    'SE Missouri State': (19, 16),
                    'UCLA': (29, 5),
                    'Arizona': (28, 6),
                    'USC': (22, 10),
                    'Colgate': (26, 8),
                    'Alabama': (29, 5),
                    'TAMU': (25, 9),
                    'Kentucky': (21, 11),
                    'Missouri': (24, 9),
                    'Tennessee': (23, 10),
                    'Mississippi State': (21, 12),
                    'Furman': (27, 7),
                    'TAMU-CC': (23, 10),
                    'Texas Southern': (14, 20),
                    'ORal Roberts': (30, 4),
                    'Louisiana': (26, 7),
                    'Gonzaga': (28, 5),
                    "Saint Mary's": (26, 7),
                    'Grand Canyon': (24, 11),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),
                    # 'Liberty': (26, 8),

                    'New Mexico State': (9, 15)}

    for index, row_info in enumerate(bt_df.iterrows()):
        team, row = row_info

        wins = games_graph.in_degree(team)
        losses = games_graph.out_degree(team)

        team = school_mapping.get(team, team)

        team_true_record = true_records.get(team, (0, 0))

        if team_true_record:
            true_wins, true_losses = team_true_record
            if wins != true_wins:
                print('Team:', team.ljust(20), 'Wins:', wins, 'Actual Wins:', true_wins)
                if losses == true_losses:
                    print()
            if losses != true_losses:
                print('Team:', team.ljust(20), 'Losses:', losses, 'Actual Losses:', true_losses)
                print()
        # else:
        #     print('True record not found for', team)
    print()

    i = 0


# def get_bracket_similarity():
#
#     picks_df = pd.read_csv('C:\\Users\\Colin\\Desktop\\March Madness\\2023\\AllPicks.csv')
#
#     brackets = list(picks_df.columns)
#     brackets.remove('Round')
#     brackets.remove('Team 1')
#     brackets.remove('Team 2')
#
#     similarity_df = pd.DataFrame(index=brackets, columns=brackets)
#
#     for bracket1, bracket2 in itertools.permutations(brackets, 2):
#         bracket1_picks = picks_df[bracket1]
#         bracket2_picks = picks_df[bracket2]
#
#         bracket1_picks = bracket1_picks.replace(to_replace=0, value=-1)
#         bracket2_picks = bracket2_picks.replace(to_replace=0, value=-1)
#
#         bracket1_picks = bracket1_picks.fillna(0)
#         bracket2_picks = bracket2_picks.fillna(0)
#         similarity = jaccard(bracket1_picks, bracket2_picks)
#
#         similarity_df.at[bracket2, bracket1] = similarity
#
#     similarity_df = similarity_df.fillna(0.0)
#     i = 0


def get_bracket_similarity(bracket_df1, bracket_df2):
    teams = bracket_df1.index

    team_win_diffs = dict()
    for team in teams:
        bracket1_team = bracket_df1[team]
        bracket2_team = bracket_df2[team]
        difference = abs(bracket1_team - bracket2_team)
        win_diff = sum(difference)
        team_win_diffs[team] = win_diff

    team_win_diffs = {team: wins for team, wins in sorted(team_win_diffs.items(), key=lambda t: t[1], reverse=True)}
    different_games = sum(team_win_diffs.values()) / 2
    return different_games
