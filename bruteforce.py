import calc

import pandas as pd


def building_invest_actions_list(actions_list: pd.DataFrame, unused_actions_list: pd.DataFrame,
                                 max_invest_price: float = 500) -> list[pd.DataFrame]:
    result = []
    try:
        action = unused_actions_list.iloc[0]
    except Exception:
        return [actions_list]
    unused_actions_list_copy = unused_actions_list.copy()
    unused_actions_list_copy.drop([action.name], axis=0, inplace=True)
    if actions_list['price'].sum() + action['price'] <= max_invest_price:
        result += building_invest_actions_list(
            pd.concat(
                [
                    actions_list,
                    action.to_frame().transpose()
                ],
                ignore_index=True
            ),
            unused_actions_list_copy,
            max_invest_price
        )
    result += building_invest_actions_list(
        actions_list,
        unused_actions_list_copy,
        max_invest_price
    )
    if len(result) >= 1:
        return result
    else:
        return [actions_list]


def get_best_invest_action_list(actions_list: pd.DataFrame, max_invest_price: float = 500) -> pd.DataFrame:
    invest_actions_list = building_invest_actions_list(
        pd.DataFrame({'price': []}),
        actions_list,
        max_invest_price
    )
    print(len(invest_actions_list))
    print("debut du tri !")
    return list_max(invest_actions_list, key=calc.action_list_balance)


def list_max(process_list: list, key=None):
    maximum = process_list[0]
    for item in process_list:
        if key is not None:
            if key(item) > key(maximum):
                maximum = item
        else:
            if item > maximum:
                maximum = item
    return maximum

