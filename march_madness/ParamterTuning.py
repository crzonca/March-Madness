import math

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss, mean_absolute_error, mean_squared_error, median_absolute_error, max_error
from sklearn.model_selection import KFold

from Projects.ncaam.march_madness import TeamSeason as Season, Tournament as Bracket, TeamRanking as Ranking


def test_alphas():
    mapping = Bracket.map_schools_to_full_name()

    possible_alphas = set(np.logspace(-4, 4, 9))
    possible_alphas = possible_alphas.union(set(np.linspace(.1, 1, 10)))
    possible_alphas = possible_alphas.union(set(np.linspace(1, 10, 10)))
    possible_alphas = sorted(list(possible_alphas))

    final_dicts = list()

    # DL all games for all years in consideration
    games_df2022 = pd.read_csv("C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\ncaamScores2022.csv")
    games_df2021 = pd.read_csv("C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\ncaamScores2021.csv")
    results_df2022 = pd.read_csv("C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\tourney_results22.csv")
    results_df2021 = pd.read_csv("C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\tourney_results21.csv")
    season_dfs = {2021: games_df2021,
                  2022: games_df2022}
    results_dfs = {2021: results_df2021,
                   2022: results_df2022}

    # For each year
    for year, year_df in season_dfs.items():
        print('Year:', year)

        graph = Season.get_games_graph(year_df)
        home_winner_graph, neut_winner_graph, away_winner_graph = Season.get_location_games_graph(year_df)

        results_df = results_dfs.get(year)

        # For each possible alpha
        for alpha in possible_alphas:
            print('\tAlpha:', alpha)

            # For each round in tournament
            for tourney_round in ['R64', 'R32', 'R16', 'R8', 'R4', 'R2']:
                round_df = results_df.loc[results_df['Round'] == tourney_round]

                # For each method
                # Calculate BTs at alpha
                original_bts = Ranking.get_bts_from_games_list(graph, alpha=alpha)
                location_bts = Ranking.get_location_adjusted_bts(graph,
                                                                 home_winner_graph,
                                                                 neut_winner_graph,
                                                                 away_winner_graph,
                                                                 alpha=alpha)
                location_bts2 = Ranking.get_location_adjusted_bts2(graph,
                                                                   home_winner_graph,
                                                                   neut_winner_graph,
                                                                   away_winner_graph,
                                                                   alpha=alpha)

                # Create n x n win chance df
                original_bts = {team: row['BT'] for team, row in original_bts.iterrows()}
                original_chances = Ranking.create_victory_chance_df(original_bts)
                home_chances, location_chances, away_chances = Ranking.create_loc_adj_victory_chance_df(location_bts)
                home_chances, location_chances2, away_chances = Ranking.create_loc_adj_victory_chance_df(location_bts2)

                for index, row in round_df.iterrows():
                    team1 = mapping.get(row['Team1'], row['Team1'])
                    team2 = mapping.get(row['Team2'], row['Team2'])
                    winner = mapping.get(row['Winner'], row['Winner'])

                    try:
                        original_prediction = Ranking.get_chance_to_beat_team(original_chances, team1, team2)
                        location_prediction = Ranking.get_chance_to_beat_team(location_chances, team1, team2)
                        location_prediction2 = Ranking.get_chance_to_beat_team(location_chances2, team1, team2)
                    except KeyError as e:
                        included_set = set(original_bts.keys())
                        team_set = {mapping.get(team, team) for team in round_df['Team1'].unique()}
                        team_set = team_set.union({mapping.get(team, team) for team in round_df['Team2'].unique()})
                        missing_set = team_set - included_set
                        print('\n'.join(original_bts.keys()))
                        print()
                        print('\n'.join(missing_set))
                        raise e
                    actual = 1 if team1 == winner else 0
                    if winner != team1 and winner != team2:
                        print('Typo')
                        print(year, index + 2, team1, team2, winner)
                        raise Exception

                    # Update BTs and win chance df based on winner
                    if actual == 1:
                        graph.add_edge(team2, team1)
                        neut_winner_graph.add_edge(team2, team1)
                    else:
                        graph.add_edge(team1, team2)
                        neut_winner_graph.add_edge(team1, team2)

                    # Compare loss function (brier? log?) for prediction with actual outcome
                    final_dicts.append({'Year': year,
                                        'Alpha': alpha,
                                        'Round': tourney_round,
                                        'Team1': team1,
                                        'Team2': team2,
                                        'Original Prediction': original_prediction,
                                        'Location Prediction': location_prediction,
                                        'Location Prediction 2': location_prediction2,
                                        'Actual': actual})

    final_df = pd.DataFrame(final_dicts)
    final_df.to_csv('C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\alphas.csv', index=False)


def compare_alphas():
    df = pd.read_csv('C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\alphas.csv')

    alphas = df['Alpha'].unique()

    results_dicts = list()

    for alpha in alphas:
        alpha_df = df.loc[df['Alpha'] == alpha]

        original_brier = brier_score_loss(alpha_df['Actual'], alpha_df['Original Prediction'])
        location_brier = brier_score_loss(alpha_df['Actual'], alpha_df['Location Prediction'])
        location_brier2 = brier_score_loss(alpha_df['Actual'], alpha_df['Location Prediction 2'])

        original_log_loss = log_loss(alpha_df['Actual'], alpha_df['Original Prediction'])
        location_log_loss = log_loss(alpha_df['Actual'], alpha_df['Location Prediction'])
        location_log_loss2 = log_loss(alpha_df['Actual'], alpha_df['Location Prediction 2'])

        results_dicts.append({'Alpha': alpha,
                              'Original Brier': original_brier,
                              'Original Log Loss': original_log_loss,
                              'Location Brier': location_brier,
                              'Location Log Loss': location_log_loss,
                              'Location Brier 2': location_brier2,
                              'Location Log Loss 2': location_log_loss2})

    results_df = pd.DataFrame(results_dicts)
    i = 0


def test_reg_alpha():
    possible_alphas = set(np.logspace(-4, 4, 9))
    possible_alphas = possible_alphas.union(set(np.linspace(.1, 1, 10)))
    possible_alphas = possible_alphas.union(set(np.linspace(1, 10, 10)))
    possible_alphas = sorted(list(possible_alphas))

    kf = KFold(n_splits=5)

    games_df = pd.read_csv('Projects/ncaam/march_madness/ncaamScores.csv')
    games_df = games_df.drop_duplicates(subset=['ID', 'Visitor', 'Visitor_ID', 'Home', 'Home_ID'])

    comparison_df = pd.DataFrame(columns=['Alpha', 'Actual', 'Prediction'])
    total_index = 0
    for alpha in possible_alphas:
        print('Alpha:', alpha)
        for fold, (train_index, test_index) in enumerate(kf.split(games_df)):
            train_games = games_df.iloc[train_index]
            ridge_df = Ranking.create_regression(games_df=train_games, alpha=alpha)

            test_games = games_df.iloc[test_index]
            for index, row in test_games.iterrows():

                away = row['Visitor']
                home = row['Home']

                if away not in ridge_df.index or home not in ridge_df.index:
                    continue

                home_actual = row['ScoreHome']
                away_actual = row['ScoreVis']

                away_off_coef = ridge_df.at[away, 'Points Coef']
                away_def_coef = ridge_df.at[away, 'Points Allowed Coef']
                home_off_coef = ridge_df.at[home, 'Points Coef']
                home_def_coef = ridge_df.at[home, 'Points Allowed Coef']
                intercept = ridge_df.at[home, 'Points Intercept']

                home_pred = intercept + home_off_coef + away_def_coef
                away_pred = intercept + away_off_coef + home_def_coef

                comparison_df.loc[total_index] = [alpha, home_actual, home_pred]
                comparison_df.loc[total_index + 1] = [alpha, away_actual, away_pred]

                total_index = total_index + 2

    comparison_df.to_csv('C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\reg_alphas.csv', index=False)


def compare_reg_alphas():
    df = pd.read_csv('C:\\Users\\Colin\\Desktop\\March Madness\\Previous MM Results\\reg_alphas.csv')
    df = df.dropna()

    alphas = df['Alpha'].unique()

    results_dicts = list()

    for alpha in alphas:
        alpha_df = df.loc[df['Alpha'] == alpha]

        mae = mean_absolute_error(alpha_df['Actual'], alpha_df['Prediction'])
        med_ae = median_absolute_error(alpha_df['Actual'], alpha_df['Prediction'])
        max_err = max_error(alpha_df['Actual'], alpha_df['Prediction'])
        mse = mean_squared_error(alpha_df['Actual'], alpha_df['Prediction'])
        rmse = math.sqrt(mse)

        results_dicts.append({'Alpha': alpha,
                              'Max Error': max_err,
                              'Median Absolute Error': med_ae,
                              'Mean Absolute Error': mae,
                              'Mean Squared Error': mse,
                              'RMSE': rmse})

    results_df = pd.DataFrame(results_dicts)
    i = 0