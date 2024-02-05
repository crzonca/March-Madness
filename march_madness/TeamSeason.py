import networkx as nx
import pandas as pd

from Projects.ncaam.march_madness import TeamsInfo


def get_games_graph(games_df=None):
    if games_df is None:
        games_df = pd.read_csv('Projects/ncaam/march_madness/ncaamScores.csv')
        games_df = games_df.drop_duplicates(subset=['ID', 'Visitor', 'Visitor_ID', 'Home', 'Home_ID'])

    graph = nx.MultiDiGraph()

    for index, row in games_df.iterrows():
        winner = row['Home'] if row['ScoreHome'] > row['ScoreVis'] else row['Visitor']
        loser = row['Visitor'] if row['ScoreHome'] > row['ScoreVis'] else row['Home']
        graph.add_edge(loser, winner)

    return graph


def get_location_games_graph(games_df=None):
    if games_df is None:
        games_df = pd.read_csv('Projects/ncaam/march_madness/ncaamScores.csv')
        games_df = games_df.drop_duplicates(subset=['ID', 'Visitor', 'Visitor_ID', 'Home', 'Home_ID'])

    home_winner_graph = nx.MultiDiGraph()
    neut_winner_graph = nx.MultiDiGraph()
    away_winner_graph = nx.MultiDiGraph()

    for index, row in games_df.iterrows():
        winner = row['Home'] if row['ScoreHome'] > row['ScoreVis'] else row['Visitor']
        loser = row['Visitor'] if row['ScoreHome'] > row['ScoreVis'] else row['Home']
        if row['Neutral'] == 1:
            neut_winner_graph.add_edge(loser, winner)
        else:
            if winner == row['Home']:
                home_winner_graph.add_edge(loser, winner)
            elif winner == row['Visitor']:
                away_winner_graph.add_edge(loser, winner)

    return home_winner_graph, neut_winner_graph, away_winner_graph


def update_graph_game(graph, winner, loser):
    winner = TeamsInfo.map_schools_to_full_name().get(winner)
    if not winner:
        print('Missing Winner')
    loser = TeamsInfo.map_schools_to_full_name().get(loser)
    if not loser:
        print('Missing Loser')
    graph.add_edge(loser, winner)
    return graph


def update_graph(graph):
    # TODO When a team wins manually add Winners and losers here
    # Paycom Wooden Legacy
    graph = update_graph_game(graph, "Saint Mary's", 'Vanderbilt')
    graph = update_graph_game(graph, 'Washington', "Saint Mary's")

    # First Four
    graph = update_graph_game(graph, 'TAMU-CC', 'SE Missouri State')
    graph = update_graph_game(graph, 'Pitt', 'Mississippi State')
    graph = update_graph_game(graph, 'FDU', 'Texas Southern')
    graph = update_graph_game(graph, 'Arizona State', 'Nevada')

    # Round of 64
    round_64_winners = []
    round_64_losers = []

    for winner, loser in zip(round_64_winners, round_64_losers):
        graph = update_graph_game(graph, winner, loser)

    # Round of 32
    round_32_winners = []
    round_32_losers = []

    for winner, loser in zip(round_32_winners, round_32_losers):
        graph = update_graph_game(graph, winner, loser)

    sweet_16_winners = []
    sweet_16_losers = []

    for winner, loser in zip(sweet_16_winners, sweet_16_losers):
        graph = update_graph_game(graph, winner, loser)

    elite_8_winners = []
    elite_8_losers = []

    for winner, loser in zip(elite_8_winners, elite_8_losers):
        graph = update_graph_game(graph, winner, loser)

    final_4_winners = []
    final_4_losers = []

    for winner, loser in zip(final_4_winners, final_4_losers):
        graph = update_graph_game(graph, winner, loser)

    # graph = update_graph_game(graph, 'UConn', 'San Diego State')

    return graph


def get_scores(games_df=None):
    if games_df is None:
        games_df = pd.read_csv('Projects/ncaam/march_madness/ncaamScores.csv')
        games_df = games_df.drop_duplicates(subset=['ID', 'Visitor', 'Visitor_ID', 'Home', 'Home_ID'])
    return games_df
