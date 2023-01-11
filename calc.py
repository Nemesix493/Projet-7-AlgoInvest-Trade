import pandas as pd


def calc_profit(actions_list: pd.DataFrame) -> pd.DataFrame:
    return actions_list.assign(
        profit=[row['price'] * (1 + row['moneyReturnRate']/100) for row in actions_list.iloc]
    )


def action_list_efficiency(actions_list: pd.DataFrame) -> float:
    return calc_profit(actions_list)['profit'].sum() / actions_list['price'].sum()


def action_list_profit(actions_list: pd.DataFrame) -> float:
    return calc_profit(actions_list)['profit'].sum() - actions_list['price'].sum()


def action_list_balance(actions_list: pd.DataFrame) -> float:
    return calc_profit(actions_list)['profit'].sum()