from controllers import main_menu
from views import TerminalViews


def main():
    view = TerminalViews()
    main_menu(view=view)


if __name__ == '__main__':
    main()

"""import pandas as pd

from controllers.inoutdata import data
from controllers.dataprocessing import optimised, bruteforce
from controllers.testing import backtest

tt = backtest.backtest(
    data.actions,
    {
        'Brute': bruteforce.get_best_invest_action_list,
        'Opti 1': optimised.get_best_invest_action_list,
        'Opti 2': optimised.test_opti_two
    },
    max_invest_price=50
)

data_data = {'Budget': 50}
for key, val in tt[0].items():
    for sub_key, sub_val in val.items():
        if sub_key != 'Budget':
            data_data[f'{key}-{sub_key}'] = [sub_val]
pd.DataFrame(data_data).to_csv('data_data.csv')"""
