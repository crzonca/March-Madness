import itertools
import math

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import nbinom, skellam, chi2
from datetime import datetime

from Projects.ncaam.march_madness import TeamsInfo
from Projects.ncaam.march_madness import Tournament as Bracket


def fit_neg_bin(df, verbose=False):
    points_df = df[['Team', 'Opponent', 'PP100', 'Is_Home', 'Is_Neutral', 'Poss_Weight']]
    points_df = points_df.rename(columns={'Team': 'Offense',
                                          'Opponent': 'Defense'})

    poisson_model = smf.glm(formula="PP100 ~ Offense + Defense + Is_Home + Is_Neutral",
                            data=points_df,
                            family=sm.families.Poisson(),
                            var_weights=points_df['Poss_Weight']).fit()

    pearson_chi2 = chi2(df=poisson_model.df_resid)
    alpha = .05
    p_value = pearson_chi2.sf(poisson_model.pearson_chi2)
    poisson_good_fit = p_value >= alpha
    if verbose:
        # print(poisson_model.summary())
        # print()

        print('Critical Value for alpha=.05:', pearson_chi2.ppf(1 - alpha))
        print('Test Statistic:              ', poisson_model.pearson_chi2)
        print('P-Value:                     ', p_value)
        if not poisson_good_fit:
            print('The Poisson Model is not a good fit for the data')
        else:
            print('The Poisson Model is a good fit for the data')
        print()

    if poisson_good_fit:
        return poisson_model, 0, True

    points_df['event_rate'] = poisson_model.mu
    points_df['auxiliary_reg'] = points_df.apply(lambda x: ((x['PP100'] - x['event_rate']) ** 2 -
                                                            x['event_rate']) / x['event_rate'], axis=1)
    aux_olsr_results = smf.ols("auxiliary_reg ~ event_rate - 1", data=points_df).fit()

    relevant_disp_param = aux_olsr_results.f_pvalue < alpha
    if not relevant_disp_param:
        print('The dispersion parameter', '(' + str(aux_olsr_results.params[0]) + ')',
              'is not statistically relevant: ', aux_olsr_results.f_pvalue)
        return poisson_model, 0, True

    if aux_olsr_results.params[0] < 0:
        print('The dispersion parameter is negative:', aux_olsr_results.params[0])
        return poisson_model, 0, True

    if verbose:
        print(aux_olsr_results.summary())
        print()

    neg_bin_model = smf.glm(formula="PP100 ~ Offense + Defense + Is_Home + Is_Neutral",
                            data=points_df,
                            family=sm.genmod.families.family.NegativeBinomial(alpha=aux_olsr_results.params[0]),
                            var_weights=points_df['Poss_Weight']).fit()

    pearson_chi2 = chi2(df=neg_bin_model.df_resid)
    p_value = pearson_chi2.sf(neg_bin_model.pearson_chi2)
    neg_bin_good_fit = p_value >= alpha
    if verbose:
        # print(neg_bin_model.summary())
        # print()

        print('Critical Value for alpha=.05:', pearson_chi2.ppf(1 - alpha))
        print('Test Statistic:              ', neg_bin_model.pearson_chi2)
        print('P-Value:                     ', p_value)
        if not neg_bin_good_fit:
            print('The Negative Binomial Model is not a good fit for the data')
        else:
            print('The Negative Binomial Model is a good fit for the data')
        print()

    return neg_bin_model, aux_olsr_results.params[0], False


def get_team_ranking(verbose=True):
    df = pd.read_csv('Projects/ncaam/march_madness/NatStat-MBB2024-Team_Statlines-2024-02-05-h11.csv')

    with open('Projects/ncaam/march_madness/Neutral Site Game IDs.txt', 'r') as neutral_file:
        neutral_game_ids = [int(game.strip()) for game in neutral_file.readlines()]
        neutral_games = df.loc[df['GameID'].isin(neutral_game_ids)]
        for index, row in neutral_games.iterrows():
            df.at[index, 'Location'] = 'N'

    df['GameDay'] = pd.to_datetime(df['GameDay'])
    df['2FM'] = df.apply(lambda r: r['FGM'] - r['3FM'], axis=1)
    df['2FA'] = df.apply(lambda r: r['FGA'] - r['3FA'], axis=1)

    df['Points'] = df.apply(lambda r: r['3FM'] * 3 + r['2FM'] * 2 + r['FTM'], axis=1)
    df['Possessions'] = df.apply(lambda r: r['FGA'] - r['OREB'] + r['TO'] + int(r['FTA'] / 2), axis=1)
    avg_poss = round(df['Possessions'].mean())
    df['Points Per Possession'] = df.apply(lambda r: 0 if r['Possessions'] == 0 else r['PTS'] / r['Possessions'],
                                           axis=1)
    df['PP100'] = df.apply(lambda r: r['Points Per Possession'] * avg_poss, axis=1)
    df['Is_Home'] = df.apply(lambda r: 1 if r['Location'] == 'H' else 0, axis=1)
    df['Is_Away'] = df.apply(lambda r: 1 if r['Location'] == 'A' else 0, axis=1)
    df['Is_Neutral'] = df.apply(lambda r: 1 if r['Location'] == 'N' else 0, axis=1)
    df['Poss_Weight'] = df.apply(lambda r: r['Possessions'] / avg_poss, axis=1)

    def get_days_ago(r):
        game_date = r['GameDay']
        today = datetime.today()
        delta = today - game_date
        days_ago = delta.days
        return days_ago

    df['Days_Ago'] = df.apply(lambda r: get_days_ago(r), axis=1)
    df['Poss_Weight'] = df.apply(lambda r: r['Poss_Weight'] * .997**r['Days_Ago'], axis=1)

    df = df[['GameDay', 'Team', 'Opponent', 'Points', 'FGM', 'FGA', '2FM', '2FA', '3FM', '3FA', 'FTM', 'FTA',
             'OREB', 'TO', 'Possessions', 'Points Per Possession', 'PP100', 'Is_Home', 'Is_Away', 'Is_Neutral',
             'Poss_Weight']]
    df = df.loc[(df['Team'] != 'ND1') & (df['Opponent'] != 'ND1')]
    df = df.dropna()

    model, dispersion, is_poisson = fit_neg_bin(df, verbose=verbose)

    off_coefs = {name.replace('Offense', '').replace('[T.', '').replace(']', ''): coef
                 for name, coef in model.params.items() if name.startswith('Offense')}
    def_coefs = {name.replace('Defense', '').replace('[T.', '').replace(']', ''): coef
                 for name, coef in model.params.items() if name.startswith('Defense')}
    intercept = model.params['Intercept']
    is_home_coef = model.params['Is_Home']
    is_neutral_coef = model.params['Is_Neutral']

    rows = list()
    for team in off_coefs.keys():
        off_coef = off_coefs.get(team, 0)
        def_coef = def_coefs.get(team, 0)

        off_adj = math.exp(intercept + off_coef)
        def_adj = math.exp(intercept + def_coef)

        adj_diff = off_adj - def_adj

        team_name_map = get_team_name_map()
        rows.append({'Team': team_name_map.get(team, team),
                     'Model': 'Poisson' if is_poisson else 'Neg Bin',
                     'Intercept': intercept,
                     'Dispersion': dispersion,
                     'Off. Coef': off_coef,
                     'Def. Coef': def_coef,
                     'Neutral Coef': is_neutral_coef,
                     'Home Coef': is_home_coef,
                     'Coef Score': off_coef - def_coef,
                     'Adj. Offense': off_adj,
                     'Adj. Defense': def_adj,
                     'Adj. Diff': adj_diff})

    results_df = pd.DataFrame(rows)
    results_df = results_df.set_index('Team', drop=True)
    results_df = results_df.sort_values(by='Coef Score', ascending=False)
    results_df.to_csv("C:\\Users\\Colin\\Desktop\\ncaam_rankings_2_04.csv")

    return results_df


def get_neg_bin_chance(mu1, mu2, alpha):
    var1 = mu1 + alpha * mu1 ** 2
    var2 = mu2 + alpha * mu2 ** 2

    p1 = mu1 / var1
    p2 = mu2 / var2

    n1 = mu1 ** 2 / (var1 - mu1)
    n2 = mu2 ** 2 / (var2 - mu2)

    nb1 = nbinom(n1, p1)
    nb2 = nbinom(n2, p2)

    min_end = min([nb1.ppf(.01), nb2.ppf(.01)])
    max_end = max([nb1.ppf(.99), nb2.ppf(.99)])

    min_end = math.floor(min_end)
    max_end = math.ceil(max_end)

    win_chance = sum([nb2.pmf(x) * nb1.sf(x) for x in np.arange(min_end, max_end + 1, 1)])
    draw_chance = sum([nb2.pmf(x) * nb1.pmf(x) for x in np.arange(min_end, max_end + 1, 1)])
    chance = win_chance / (1 - draw_chance)

    return chance


def get_skellam_chance(mu1, mu2):
    skel = skellam(mu1, mu2)
    win_chance = skel.sf(0)
    draw_chance = skel.pmf(0)
    chance = win_chance / (1 - draw_chance)

    return chance


def create_chance_df(reg_df, use_all=True):
    teams = reg_df.index if use_all else Bracket.get_teams_by_seed()
    school_to_full = TeamsInfo.map_schools_to_full_name()
    chances_df = pd.DataFrame(index=[school_to_full.get(team, team) for team in teams],
                              columns=[school_to_full.get(team, team) for team in teams])
    is_poisson = reg_df['Model'][0] == 'Poisson'
    intercept = reg_df['Intercept'].mean()
    dispersion = reg_df['Dispersion'].mean()
    for team1, team2 in itertools.combinations(teams, 2):
        mu1 = math.exp(intercept + reg_df.at[team1, 'Off. Coef'] + reg_df.at[team2, 'Def. Coef'] +
                       reg_df.at[team2, 'Neutral Coef'])
        mu2 = math.exp(intercept + reg_df.at[team2, 'Off. Coef'] + reg_df.at[team1, 'Def. Coef'] +
                       reg_df.at[team2, 'Neutral Coef'])

        team1 = school_to_full.get(team1, team1)
        team2 = school_to_full.get(team2, team2)

        if is_poisson:
            chances_df.at[team2, team1] = get_skellam_chance(mu1, mu2)
            chances_df.at[team1, team2] = get_skellam_chance(mu2, mu1)
        else:
            chances_df.at[team2, team1] = get_neg_bin_chance(mu1, mu2, dispersion)
            chances_df.at[team1, team2] = get_neg_bin_chance(mu2, mu1, dispersion)

    return chances_df


def get_team_name_map():
    return {'Texas A&M-Corpus Christi': 'TAMU-CC',
            'Southeast Missouri State': 'SE Missouri State',
            'College of Charleston': 'Charleston',
            'North Carolina State': 'NC State',
            'UC Santa Barbara': 'UCSB',
            'Fairleigh Dickinson': 'FDU',
            'Florida Atlantic': 'FAU',
            'Louisiana-Lafayette': 'Louisiana',
            'Sam Houston': 'Sam Houston State',
            'Southern California': 'USC',
            'Miami (Fla.)': 'Miami',
            'Pittsburgh': 'Pitt',
            'Texas A&M': 'TAMU',
            'Saint Mary`s': "Saint Mary's",
            'Saint John`s': "Saint John's",
            'Connecticut': 'UConn',
            'Texas Christian': 'TCU'}
