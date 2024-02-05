# TODO Remove
def fit_model(df, model_str):
    num_comp = len(model_str.split('+'))
    print(num_comp, model_str)
    points_df = df[['Team', 'Opponent', 'PP100', 'Is_Home', 'Is_Away', 'Is_Neutral', 'Poss_Weight']]
    points_df = points_df.rename(columns={'Team': 'Offense',
                                          'Opponent': 'Defense'})

    try:
        poisson_model = smf.glm(formula=model_str,
                                data=points_df,
                                family=sm.families.Poisson(),
                                var_weights=points_df['Poss_Weight']).fit(disp=1)

        pearson_chi2 = chi2(df=poisson_model.df_resid)
        alpha = .05
        p_value = pearson_chi2.sf(poisson_model.pearson_chi2)
        poisson_good_fit = p_value >= alpha

        poisson_results = {'Model Type': 'Poisson',
                           'Model': model_str,
                           'AIC': poisson_model.aic,
                           'BIC': poisson_model.bic_llf,
                           'Dispersion': 0,
                           'Num Obs': poisson_model.nobs,
                           'Components': num_comp,
                           'DF Residuals': poisson_model.df_resid,
                           'DF Model': poisson_model.df_model,
                           'Total DF': poisson_model.df_resid + poisson_model.df_model,
                           'Log Likelihood': poisson_model.llf,
                           'Deviance': poisson_model.deviance,
                           'Pearson Chi2 Statistic': poisson_model.pearson_chi2,
                           'Pearson Chi2 Critical Value': pearson_chi2.ppf(1 - alpha),
                           'Pearson Chi2 P-Value': p_value}
    except ValueError as e:
        poisson_results = {'Model Type': 'Poisson',
                           'Model': model_str,
                           'AIC': np.nan,
                           'BIC': np.nan,
                           'Dispersion': np.nan,
                           'Num Obs': np.nan,
                           'Components': np.nan,
                           'DF Residuals': np.nan,
                           'DF Model': np.nan,
                           'Total DF': np.nan,
                           'Log Likelihood': np.nan,
                           'Deviance': np.nan,
                           'Pearson Chi2 Statistic': np.nan,
                           'Pearson Chi2 Critical Value': np.nan,
                           'Pearson Chi2 P-Value': np.nan}

        neg_bin_results = {'Model Type': 'Negative Binomial',
                           'Model': model_str,
                           'AIC': np.nan,
                           'BIC': np.nan,
                           'Dispersion': np.nan,
                           'Num Obs': np.nan,
                           'Components': np.nan,
                           'DF Residuals': np.nan,
                           'DF Model': np.nan,
                           'Total DF': np.nan,
                           'Log Likelihood': np.nan,
                           'Deviance': np.nan,
                           'Pearson Chi2 Statistic': np.nan,
                           'Pearson Chi2 Critical Value': np.nan,
                           'Pearson Chi2 P-Value': np.nan}

        return poisson_results, neg_bin_results

    # ----------------------------------------------------------------------

    points_df['event_rate'] = poisson_model.mu
    points_df['auxiliary_reg'] = points_df.apply(lambda x: ((x['PP100'] - x['event_rate']) ** 2 - x['event_rate']) / x['event_rate'], axis=1)
    aux_olsr_results = smf.ols("auxiliary_reg ~ event_rate - 1", data=points_df).fit()

    relevant_disp_param = aux_olsr_results.f_pvalue < alpha
    if not relevant_disp_param or aux_olsr_results.params[0] <= 0:
        dispersion_param = 1e-16
    else:
        dispersion_param = aux_olsr_results.params[0]

    # ----------------------------------------------------------------------

    try:
        neg_bin_model = smf.glm(formula=model_str,
                                data=points_df,
                                family=sm.genmod.families.family.NegativeBinomial(alpha=dispersion_param),
                                var_weights=points_df['Poss_Weight']).fit()

        pearson_chi2 = chi2(df=neg_bin_model.df_resid)
        p_value = pearson_chi2.sf(neg_bin_model.pearson_chi2)
        neg_bin_good_fit = p_value >= alpha

        neg_bin_results = {'Model Type': 'Negative Binomial',
                           'Model': model_str,
                           'AIC': neg_bin_model.aic,
                           'BIC': neg_bin_model.bic_llf,
                           'Dispersion': dispersion_param,
                           'Num Obs': neg_bin_model.nobs,
                           'Components': num_comp,
                           'DF Residuals': neg_bin_model.df_resid,
                           'DF Model': neg_bin_model.df_model,
                           'Total DF': neg_bin_model.df_resid + neg_bin_model.df_model,
                           'Log Likelihood': neg_bin_model.llf,
                           'Deviance': neg_bin_model.deviance,
                           'Pearson Chi2 Statistic': neg_bin_model.pearson_chi2,
                           'Pearson Chi2 Critical Value': pearson_chi2.ppf(1 - alpha),
                           'Pearson Chi2 P-Value': p_value}
    except ValueError as e:
        neg_bin_results = {'Model Type': 'Negative Binomial',
                           'Model': model_str,
                           'AIC': np.nan,
                           'BIC': np.nan,
                           'Dispersion': np.nan,
                           'Num Obs': np.nan,
                           'DF Residuals': np.nan,
                           'DF Model': np.nan,
                           'Total DF': np.nan,
                           'Log Likelihood': np.nan,
                           'Deviance': np.nan,
                           'Pearson Chi2 Statistic': np.nan,
                           'Pearson Chi2 Critical Value': np.nan,
                           'Pearson Chi2 P-Value': np.nan}

    return poisson_results, neg_bin_results


# TODO Update and Remove
def likelihood_ratio(llf_full, llf_reduced, df_full, df_reduced):
    lr_df = df_reduced - df_full
    lr_stat = -2 * (llf_reduced - llf_full)

    chi2_dist = chi2(df=lr_df)
    lr_pvalue = chi2_dist.sf(lr_stat)

    # print('Degrees of Freedom:          ', lr_df)
    # print('Critical Value for alpha=.05:', chi2_dist.ppf(1 - alpha))
    # print('Test Statistic:              ', lr_stat)
    # print('P-Value:                     ', lr_pvalue)

    return lr_pvalue


def compare_models():
    # with open('C:\\Users\\Colin\\Desktop\\results_graph.json', 'r') as f:
    #     data = json.load(f)
    #     g = nx.node_link_graph(data)
    #     sinks = [node for node, out_degree in g.out_degree() if out_degree == 0]
    #     for sink in sinks:
    #         print(sink)
    #     i = 0
    alpha = 0.05

    results_df = pd.read_csv('C:\\Users\\Colin\\Desktop\\model_results_final.csv')

    def is_subset(model_str1, model_str2):
        model1_comps = model_str1.split(' ~ ')[-1]
        model1_comps = set(model1_comps.split(' + '))

        model2_comps = model_str2.split(' ~ ')[-1]
        model2_comps = set(model2_comps.split(' + '))

        return model2_comps.intersection(model1_comps) == model1_comps

    model_nums = results_df['Model Number'].unique()

    graph = nx.MultiDiGraph()

    for model_num1, model_num2 in reversed(list(itertools.combinations(model_nums, 2))):
        model1 = results_df.loc[results_df['Model Number'] == model_num1].squeeze()
        model2 = results_df.loc[results_df['Model Number'] == model_num2].squeeze()

        try:
            if model1['Model Type'] != model2['Model Type']:
                continue
        except ValueError as e:
            print(e)

        model_formula1 = model1['Model']
        model_formula2 = model2['Model']

        model1_num_comps = len(model_formula1.split(' + '))
        model2_num_comps = len(model_formula2.split(' + '))

        if model1_num_comps > model2_num_comps:
            if is_subset(model_formula2, model_formula1):
                model2_llf = model2['Log Likelihood']
                model1_llf = model1['Log Likelihood']

                model2_df = model2['DF Residuals']
                model1_df = model1['DF Residuals']
                lr_pvalue = likelihood_ratio(model1_llf, model2_llf, model1_df, model2_df)

                if lr_pvalue < alpha:
                    print('Model', model_num1, 'is better than', model_num2)
                    graph.add_edge(str(model_num2), str(model_num1))
                else:
                    print('No evidence the two models are different: Model', model_num2, 'is better than', model_num1)

        elif model1_num_comps < model2_num_comps:
            if is_subset(model_formula1, model_formula2):
                model2_llf = model2['Log Likelihood']
                model1_llf = model1['Log Likelihood']

                model2_df = model2['DF Residuals']
                model1_df = model1['DF Residuals']
                lr_pvalue = likelihood_ratio(model2_llf, model1_llf, model2_df, model1_df)

                if lr_pvalue < alpha:
                    print('Model', model_num2, 'is better than', model_num1)
                    graph.add_edge(str(model_num1), str(model_num2))
                else:
                    print('No evidence the two models are different: Model', model_num1, 'is better than', model_num2)

    with open('C:\\Users\\Colin\\Desktop\\results_graph_final.json', 'w') as file:
        json_str = nx.node_link_data(graph)
        json.dump(json_str, file, indent=4)

    i = 0




with open("C:\\Users\\Colin\\Desktop\\possible_models3.txt", 'r') as f:
    possible_models = f.readlines()

results_rows = list()
for model_str in possible_models:
    model_str = model_str.strip()
    poisson_results, neg_bin_results = fit_model(df, model_str)
    results_rows.append(poisson_results)
    results_rows.append(neg_bin_results)
results_df = pd.DataFrame(results_rows)
results_df.to_csv('C:\\Users\\Colin\\Desktop\\model_results_final.csv')


# TODO Remove
def model_combos():
    # 'Offense',  # The team
    # 'Defense',  # The team that is defending them

    # params = ['Is_Home',                # If the team is at home                    (general advantage)
    #           'Is_Away',                # If the team is on the road                (general disadvantage)
    #           'Is_Neutral',             # If the team is playing on a neutral court (general difference)
    #           'Offense:Is_Home',        # How a specific team performs at home
    #           'Offense:Is_Away',        # How a specific team performs on the road
    #           'Offense:Is_Neutral',     # How a specific team performs on a neutral court
    #           'Defense:Is_Home',        # How teams perform at home when playing a specific opponent
    #           'Defense:Is_Away',        # How teams perform on the road when playing a specific opponent
    #           'Defense:Is_Neutral']     # How teams perform on a neutral court when playing a specific opponent

    params = ['Is_Home',
              'Is_Away',
              'Is_Neutral',
              'Offense:Is_Home + Defense:Is_Home',  # Is Home
              'Offense:Is_Away + Defense:Is_Away',  # Is Away
              'Offense:Is_Home + Defense:Is_Away',  # At Offense
              'Offense:Is_Away + Defense:Is_Home',  # At Defense
              'Offense:Is_Neutral + Defense:Is_Neutral']
    for param_count in reversed(range(1, 9)):
        for param_combo in itertools.combinations(params, param_count):
            additional_params = ' + '.join(param_combo)
            all_params = additional_params.split(' + ')
            if all_params.count('Offense:Is_Home') > 1:
                continue
            if all_params.count('Offense:Is_Away') > 1:
                continue
            if all_params.count('Defense:Is_Home') > 1:
                continue
            if all_params.count('Defense:Is_Away') > 1:
                continue
            if 'Is_Home' in all_params and ('Offense:Is_Home' in all_params or 'Defense:Is_Home' in all_params):
                continue
            if 'Is_Away' in all_params and ('Offense:Is_Away' in all_params or 'Defense:Is_Away' in all_params):
                continue
            if 'Is_Neutral' in all_params and ('Offense:Is_Neutral' in all_params or 'Defense:Is_Neutral' in all_params):
                continue
            print('PP100 ~ Offense + Defense +', ' + '.join(param_combo))

            # TODO Remove
            def fix_neutral_games():
                df = pd.read_csv('Projects/ncaam/march_madness/NatStat-MBB2024-Team_Statlines-2024-01-16-h11.csv')
                correction_df = pd.read_csv("C:\\Users\\Colin\\Desktop\\neutral_sites.csv")

                for index, row in correction_df.iterrows():
                    corresponding_game1 = df.loc[(df['Team'] == row['Team1']) &
                                                 (df['Opponent'] == row['Team2']) &
                                                 (df['GameDay'] == row['Date'])]

                    if len(corresponding_game1) != 1:
                        print(row['Team1'].ljust(20), row['Team2'].ljust(20), row['Date'])
                        continue

                    corresponding_game2 = df.loc[(df['Team'] == row['Team2']) &
                                                 (df['Opponent'] == row['Team1']) &
                                                 (df['GameDay'] == row['Date'])]

                    if len(corresponding_game2) != 1:
                        print(row['Team1'].ljust(20), row['Team2'].ljust(20), row['Date'])
                        continue

                    cg1_index = corresponding_game1.index[0]
                    cg2_index = corresponding_game2.index[0]

                    df.at[cg1_index, 'Location'] = 'N'
                    df.at[cg2_index, 'Location'] = 'N'

                    j = 0

                neutral_games = df.loc[df['Location'] == 'N']
                print('\n'.join([str(game_id) for game_id in neutral_games['GameID'].unique()]))

                df.to_csv('Projects/ncaam/march_madness/NatStat-MBB2024-Team_Statlines-2024-01-16-h11-2.csv')

                i = 0
