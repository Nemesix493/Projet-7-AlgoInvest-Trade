import pandas as pd


def calc_balances(actions_list: pd.DataFrame) -> pd.DataFrame:
    return actions_list.assign(
        balances=[row['price'] * (1 + row['efficiency']/100) for row in actions_list.iloc]
    )


def calc_profits(actions_list: pd.DataFrame) -> pd.DataFrame:
    return actions_list.assign(
        profits=[row['balances'] - row['price'] for row in calc_balances(actions_list).iloc]
    )


def action_list_efficiency(actions_list: pd.DataFrame) -> float:
    return calc_balances(actions_list)['balances'].sum() / actions_list['price'].sum()


def action_list_profit(actions_list: pd.DataFrame) -> float:
    return calc_balances(actions_list)['balances'].sum() - actions_list['price'].sum()


def action_list_balance(actions_list: pd.DataFrame, invested: float) -> float:
    return calc_profits(actions_list)['profits'].sum() + invested


def actions_list_report(actions_list: pd.DataFrame, invested) -> pd.DataFrame:
    return pd.DataFrame({
        'Profits': [action_list_profit(actions_list)],
        'Efficiency': [action_list_efficiency(actions_list)],
        'Balance': [action_list_balance(actions_list, invested)],
        'Total invested': [actions_list['price'].sum()]
    })


def clean_data_frame(actions_list: pd.DataFrame) -> pd.DataFrame:
    actions_list_result = actions_list.copy()
    for action in actions_list_result.iloc:
        if action['price'] <= 0 or action['efficiency'] <= 0:
            actions_list_result = actions_list_result.drop([action.name])
    return actions_list_result
