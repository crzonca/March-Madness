from Projects.ncaam.march_madness import TeamSeason as Season, Tournament as Bracket, TablePrinter as Table, \
    TeamRanking as Ranking, ScoringSystems as Scoring

from Projects.ncaam.march_madness import bracket as br

from Projects.ncaam.march_madness import Model1, Model2, Model3, Model4, Model5, Validation


def march_madness(model=1):
    br.mm_bracket()

    # Model 1: Pure BT
    # Model 2: BT with Home Court Advantage
    # Model 3: BT with Home Court Advantage and Road Disadvantage
    # Model 4: BT with Offset for Conference Strength
    # Model 5: Negative Binomial Regression

    # Method 1: Best Team
    # Method 2: Chance to make each round
    # Method 3: Expected points from each round
    # Method 4: Expected points from each round; eliminating teams taking best overall first
    #   Struggles with teams that will do well in first rounds but will not later
    # Method 5: Expected points from each round; eliminating teams taking best at each game
    #   Struggles with teams that will do well in later rounds but not to start
    # Method 6: Expected points from each round; eliminating worse team each round
    if not 1 <= model <= 5:
        model = 1

    matchups = Bracket.get_matchup_graph()

    graph = Season.get_games_graph()
    graph = Season.update_graph(graph)

    home_winner_graph, neut_winner_graph, away_winner_graph = Season.get_location_games_graph()
    neut_winner_graph = Season.update_graph(neut_winner_graph)

    if model == 2:
        print('Team Rankings Adjusting for Home Court Advantage (1)')
        ranking_func = Model2.get_team_ranking
        ranking_func_args = (graph, home_winner_graph, neut_winner_graph, away_winner_graph)

        chance_df_func = Model2.create_chance_df
    elif model == 3:
        print('Team Rankings Adjusting for Home Court Advantage and Road Disadvantage (1)')
        ranking_func = Model3.get_team_ranking
        ranking_func_args = (graph, home_winner_graph, neut_winner_graph, away_winner_graph)

        chance_df_func = Model3.create_chance_df
    elif model == 4:
        print('Team Rankings Adjusting for Conference (1)')
        ranking_func = Model4.get_team_ranking
        ranking_func_args = (graph,)

        chance_df_func = Model4.create_chance_df
    elif model == 5:
        print('Team Rankings Based on Adjusted Score (1)')
        ranking_func = Model5.get_team_ranking
        ranking_func_args = ()

        chance_df_func = Model5.create_chance_df
    else:
        print('Overall Team Rankings: Game by Game Matchup (1)')
        ranking_func = Model1.get_team_ranking
        ranking_func_args = (graph,)

        chance_df_func = Model1.create_chance_df

    # Get each teams ranking and their chance to win against every other team according to the model
    ranking_df = ranking_func(*ranking_func_args)
    chances_df = chance_df_func(ranking_df)

    if model == 2 or model == 3:
        home_chances_df, chances_df, away_chances_df = chances_df

    # Show team rankings
    Table.print_team_rankings(ranking_df, graph, ranking_column='Coef Score' if model == 5 else 'BT')

    # DFs
    march_madness_chance_df = Bracket.calculate_game_chances(chances_df, matchups)
    march_madness_points_df = Bracket.calculate_expected_points(march_madness_chance_df)
    # march_madness_points_df_eliminating = Bracket.calculate_expected_points_eliminating(chances_df, matchups)
    # march_madness_points_df_greedy = Bracket.calculate_expected_points_greedy(chances_df, matchups)
    march_madness_points_df_best = Bracket.calculate_expected_points_best(chances_df, ranking_df, matchups)

    # Create Choice DFs
    overall_chance_choices = Scoring.create_choice_df_overall_chance(chances_df, matchups)
    points_choices = Scoring.create_choice_df_most_points(chances_df, matchups)
    # points_eliminating_choices = Scoring.create_choice_df_most_points_eliminating(chances_df, matchups)
    # points_greedy_choices = Scoring.create_choice_df_most_points_greedy(chances_df, matchups)
    points_best_choices = Scoring.create_choice_df_most_points_best(chances_df, ranking_df, matchups)

    # Create Topologies
    overall_chance_topology = Scoring.create_topology(march_madness_chance_df, overall_chance_choices)
    points_topology = Scoring.create_topology(march_madness_points_df, points_choices)
    # points_elim_topology = Scoring.create_topology(march_madness_points_df_eliminating, points_eliminating_choices)
    # points_greedy_topology = Scoring.create_topology(march_madness_points_df_greedy, points_greedy_choices)
    points_best_topology = Scoring.create_topology(march_madness_points_df_best, points_best_choices)

    best_bracket = Scoring.completed_bracket(Scoring.create_choice_df_better_head_to_head(chances_df), matchups)
    chance_bracket = Scoring.completed_bracket(overall_chance_choices, matchups)
    points_bracket = Scoring.completed_bracket(points_choices, matchups)
    # points_eliminating_bracket = Scoring.completed_bracket(points_eliminating_choices, matchups)
    # points_greedy_bracket = Scoring.completed_bracket(points_greedy_choices, matchups)
    points_best_bracket = Scoring.completed_bracket(points_best_choices, matchups)
    actual_bracket = Scoring.create_true_bracket_df(matchups)

    print('Best')
    Validation.get_bracket_similarity(actual_bracket, best_bracket)
    print('Overall Chance')
    Validation.get_bracket_similarity(actual_bracket, chance_bracket)
    print('Most Points')
    Validation.get_bracket_similarity(actual_bracket, points_bracket)
    # print('Most Points Eliminating')
    # Validation.get_bracket_similarity(actual_bracket, points_eliminating_bracket)
    # print('Most Points Greedy')
    # Validation.get_bracket_similarity(actual_bracket, points_greedy_bracket)
    print('Most Points Best')
    Validation.get_bracket_similarity(actual_bracket, points_best_bracket)
    print('Identical')
    Validation.get_bracket_similarity(actual_bracket, actual_bracket.copy())

    # Show round chances
    print('Chance For Each Team To Make Each Round (2)')
    Table.print_team_chances(overall_chance_topology.copy())

    # Show expected points
    print('Expected Points For Each Team For Making Each Round (3)')
    Table.print_team_points(points_topology.copy())

    # # Show expected points from best picks
    # print('Expected Points For Each Team Eliminating Teams Moving Down (4)')
    # Table.print_team_points(points_elim_topology.copy())
    #
    # # Show expected points from best picks
    # print('Expected Points For Each Team Eliminating Teams Moving Up (5)')
    # Table.print_team_points(points_greedy_topology.copy())

    # Show expected points from best picks
    print('Expected Points For Each Team Eliminating Teams Taking Best One (4)')
    Table.print_team_points(points_best_topology.copy())

    # Show the conference rankings
    if model == 4:
        print('Conference Rankings')
        Table.print_conference_rankings(ranking_df)

        print('Team Rankings Within Conference')
        Table.print_intraconf_rankings(ranking_df, graph)
