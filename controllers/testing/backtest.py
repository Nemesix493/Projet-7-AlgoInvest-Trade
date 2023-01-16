import time

import pandas as pd

from controllers.dataprocessing import calc


def backtest(actions_list: pd.DataFrame, test_functions: dict,
             max_invest_price: float = 500) -> tuple[pd.DataFrame, dict[pd.DataFrame]]:
    data = {}
    actions_lists = {}
    for key, val in test_functions.items():
        start = time.time()
        invest_action_list = val(actions_list, max_invest_price)
        stop = time.time()
        actions_lists[key] = invest_action_list
        data[key] = {
            'Time': stop-start,
            'Budget': max_invest_price,
            'Invested': invest_action_list['price'].sum(),
            'Efficiency': calc.action_list_efficiency(invest_action_list),
            'Profit': calc.action_list_profit(invest_action_list),
            'Balance': calc.action_list_balance(invest_action_list)
        }
    return pd.DataFrame(data), actions_lists

    """data_report = pd.DataFrame({'Brute time / Opti time': []})
    print(f'\nOptimised calculating for {(i + 1) * step} €')
    opti_time = time.time()
    opti_actions_list = optimised.get_best_invest_action_list(data.actions, (i + 1) * step).sort_values(
        by=['price'])
    opti_time = time.time() - opti_time
    print(f'Bruteforce calculating for {(i + 1) * step} €')
    brute_time = time.time()
    brute_actions_list = bruteforce.get_best_invest_action_list(data.actions, (i + 1) * step).sort_values(
        by=['price'])
    brute_time = time.time() - brute_time
    data_report = pd.concat(
        [
            data_report,
            pd.DataFrame({
                'Investing': [(i + 1) * step],
                'Bruteforce time': [brute_time],
                'Bruteforce balance': [calc.action_list_balance(brute_actions_list)],
                'Optimised time': [opti_time],
                'Optimised balance': [calc.action_list_balance(opti_actions_list)],
                'Brute time / Opti time': [brute_time / opti_time],
                'Bruteforce balance - Optimised balance': [
                    calc.action_list_balance(opti_actions_list) - calc.action_list_balance(brute_actions_list)
                ],
                '(Brute time / Opti time) Mean': [
                    pd.concat(
                        [
                            data_report['Brute time / Opti time'].to_frame(),
                            pd.DataFrame({
                                'Brute time / Opti time': [brute_time / opti_time]
                            })
                        ]
                    )['Brute time / Opti time'].mean()
                ]
            })
        ],
        ignore_index=True
    )
    data_report.to_csv('report.csv')"""