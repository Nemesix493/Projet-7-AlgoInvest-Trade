import time

import pandas as pd

import calc
import data
import bruteforce
import optimised

step = 50
step_nbr = 20

data_report = pd.DataFrame({'Brute time / Opti time': []})
for i in range(step_nbr):
    print(f'\nOptimised calculating for {(i + 1) * step} €')
    opti_time = time.time()
    opti_actions_list = optimised.get_best_invest_action_list(data.actions, (i + 1) * step).sort_values(by=['price'])
    opti_time = time.time() - opti_time
    print(f'Bruteforce calculating for {(i + 1) * step} €')
    brute_time = time.time()
    brute_actions_list = bruteforce.get_best_invest_action_list(data.actions, (i + 1) * step).sort_values(by=['price'])
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
                'Brute time / Opti time': [brute_time/opti_time],
                'Bruteforce balance - Optimised balance': [
                    calc.action_list_balance(opti_actions_list) - calc.action_list_balance(brute_actions_list)
                ],
                '(Brute time / Opti time) Mean': [
                    pd.concat(
                        [
                            data_report['Brute time / Opti time'].to_frame(),
                            pd.DataFrame({
                                'Brute time / Opti time': [brute_time/opti_time]
                            })
                        ]
                    )['Brute time / Opti time'].mean()
                ]
            })
        ],
        ignore_index=True
    )
    data_report.to_csv('report.csv')
