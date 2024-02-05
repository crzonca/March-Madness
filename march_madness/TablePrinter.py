from prettytable import PrettyTable

from Projects.ncaam.march_madness import TeamsInfo
from Projects.ncaam.march_madness import Tournament as Bracket, TeamRanking as Ranking


def print_team_rankings(topo_df, games_graph, ranking_column='BT'):
    school_mapping = TeamsInfo.map_schools_to_full_name()
    teams = Bracket.get_teams_by_seed(use_full_names=ranking_column == 'BT')
    topo_df = Ranking.get_tiers(topo_df, ranking_column=ranking_column)
    topo_df = topo_df.loc[teams]

    topo_df = topo_df.sort_values(by=ranking_column, kind='mergesort', ascending=False)
    topo_df = topo_df.reset_index(names='Team')
    topo_df = topo_df.reset_index(names='Rank')
    topo_df['Rank'] = topo_df.apply(lambda r: r['Rank'] + 1, axis=1)
    columns = list(topo_df.columns)
    if 'Var' in columns:
        topo_df = topo_df.drop(columns=['Var'])
    if 'Model' in columns:
        topo_df = topo_df.drop(columns=['Model'])
    if 'Intercept' in columns:
        topo_df = topo_df.drop(columns=['Intercept'])
    if 'Dispersion' in columns:
        topo_df = topo_df.drop(columns=['Dispersion'])
    if 'Neutral Coef' in columns:
        topo_df = topo_df.drop(columns=['Neutral Coef'])
    if 'Home Coef' in columns:
        topo_df = topo_df.drop(columns=['Home Coef'])

    topo_df['Team'] = topo_df.apply(lambda r: school_mapping.get(r['Team'], r['Team']), axis=1)
    topo_df['Record'] = topo_df.apply(lambda r: str(games_graph.in_degree(r['Team'])) + ' - ' +
                                                str(games_graph.out_degree(r['Team'])), axis=1)
    school_mapping = TeamsInfo.map_full_names_to_school()
    topo_df['Team'] = topo_df.apply(lambda r: school_mapping.get(r['Team'], r['Team']), axis=1)

    columns = list(topo_df.columns)
    topo_df = topo_df[columns[:-2] + ['Record', 'Tier']]

    columns = list(topo_df.columns)
    table = PrettyTable(columns)
    table.float_format = '0.3'

    for index, row in topo_df.iterrows():
        table_row = list()
        table_row.extend([item for i, item in list(row.items())])
        table.add_row(table_row)

    # Print the table
    print(table)
    print()
    pass


def print_team_chances(topo_df):
    school_mapping = TeamsInfo.map_full_names_to_school()
    topo_df.loc['TOTAL'] = topo_df.sum() / 100.0
    topo_df = topo_df.reset_index(names='Team')

    topo_df['Team'] = topo_df.apply(lambda r: school_mapping.get(r['Team'], r['Team']), axis=1)

    columns = list(topo_df.columns)
    table = PrettyTable(columns)
    table.float_format = '0.3'

    for index, row in topo_df.iterrows():
        table_row = list()
        table_row.append(row['Team'])
        table_row.extend([f'{row[column] * 100:.3f}' for column in columns[1:]])
        table.add_row(table_row)

    # Print the table
    print(table)
    print()


def print_team_points(topo_df):
    school_mapping = TeamsInfo.map_full_names_to_school()
    topo_df.loc['TOTAL'] = topo_df.sum()
    topo_df = topo_df.reset_index(names='Team')

    topo_df['Team'] = topo_df.apply(lambda r: school_mapping.get(r['Team'], r['Team']), axis=1)

    columns = list(topo_df.columns)
    table = PrettyTable(columns)
    table.float_format = '0.3'

    for index, row in topo_df.iterrows():
        table_row = list()
        table_row.extend([item for i, item in list(row.items())])
        table.add_row(table_row)

    # Print the table
    print(table)
    print()


def print_conference_rankings(conf_bt_df):
    teams = Bracket.get_teams_by_seed()
    conf_bt_df = conf_bt_df.loc[teams]

    table = PrettyTable(['Rank', 'Conference', 'BT'])
    table.float_format = '0.3'

    bt_df = conf_bt_df[['Conference', 'Conference BT']]
    bt_df = bt_df.drop_duplicates(subset=['Conference', 'Conference BT'])
    bt_df = bt_df.sort_values(by='Conference BT', kind='mergesort', ascending=False)
    bt_df = bt_df.reset_index()

    for index, row in bt_df.iterrows():
        table_row = list()

        table_row.append(index + 1)
        table_row.append(row['Conference'])
        table_row.append(row['Conference BT'])

        table.add_row(table_row)

    # Print the table
    print(table)
    print()


def print_intraconf_rankings(conf_bt_df, games_graph):
    conf_bt_df = conf_bt_df.sort_values(by=['Conference BT', 'Team BT'], kind='mergesort', ascending=[False, False])
    conf_ranking_df = conf_bt_df[['Conference', 'Conference BT']]
    conf_ranking_df = conf_ranking_df.drop_duplicates(subset=['Conference', 'Conference BT'])
    conf_ranking_df = conf_ranking_df.sort_values(by='Conference BT', kind='mergesort', ascending=False)
    conf_ranking_df = conf_ranking_df.reset_index()

    for index, conference in conf_ranking_df['Conference'].items():
        print(conference)

        conf_df = conf_bt_df.loc[conf_bt_df['Conference'] == conference]

        table = PrettyTable(['Rank', 'Team', 'Record', 'BT'])
        table.float_format = '0.3'

        school_mapping = TeamsInfo.map_full_names_to_school()

        for index, row_info in enumerate(conf_df.iterrows()):
            table_row = list()
            team, row = row_info

            wins = games_graph.in_degree(team)
            losses = games_graph.out_degree(team)

            if conference == 'Independent' and wins + losses < 20:
                continue

            table_row.append(index + 1)
            table_row.append(school_mapping.get(team, team))

            table_row.append(str(wins) + ' - ' + str(losses))
            table_row.append(row['BT'])

            table.add_row(table_row)

        # Print the table
        print(table)
        print()


def print_adjusted_score(ridge_df, games_graph):
    teams = Bracket.get_teams_by_seed()
    ridge_df = ridge_df.loc[teams]

    ridge_df = ridge_df.sort_values(by='Adjusted Point Diff', kind='mergesort', ascending=False)
    table = PrettyTable(['Rank', 'Team', 'Record', 'Adj Points', 'Adj Points Allowed', 'Adj Point Diff'])
    table.float_format = '0.3'

    school_mapping = TeamsInfo.map_full_names_to_school()

    for index, row_info in enumerate(ridge_df.iterrows()):
        table_row = list()

        team, row = row_info

        table_row.append(index + 1)
        table_row.append(school_mapping.get(team, team))

        wins = games_graph.in_degree(team)
        losses = games_graph.out_degree(team)

        table_row.append(str(wins) + ' - ' + str(losses))
        table_row.append(row['Adjusted Points'])
        table_row.append(row['Adjusted Points Allowed'])
        table_row.append(row['Adjusted Point Diff'])

        table.add_row(table_row)

    # Print the table
    print(table)
    print()
