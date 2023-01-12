import pandas as pd


def calc_balances(actions_list: pd.DataFrame) -> pd.DataFrame:
    return actions_list.assign(
        balances=[row['price'] * (1 + row['moneyReturnRate']/100) for row in actions_list.iloc]
    )


def calc_profits(actions_list: pd.DataFrame) -> pd.DataFrame:
    return actions_list.assign(
        profits=[row['balances'] - row['price'] for row in calc_balances(actions_list).iloc]
    )


def action_list_efficiency(actions_list: pd.DataFrame) -> float:
    return calc_balances(actions_list)['balances'].sum() / actions_list['price'].sum()


def action_list_profit(actions_list: pd.DataFrame) -> float:
    return calc_balances(actions_list)['balances'].sum() - actions_list['price'].sum()


def action_list_balance(actions_list: pd.DataFrame) -> float:
    return calc_balances(actions_list)['balances'].sum()
