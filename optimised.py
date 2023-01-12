import pandas as pd

import calc


def get_best_invest_action_list(actions_list: pd.DataFrame, max_invest_price: float = 500) -> pd.DataFrame:
    return max(
        building_invest_actions_list(pd.DataFrame({'price': []}), actions_list, max_invest_price),
        key=calc.action_list_balance
    )


def building_invest_actions_list(actions_list: pd.DataFrame, unused_actions_list: pd.DataFrame,
                                 max_invest_price: float = 500) -> list[pd.DataFrame]:
    try:
        next_min = actions_list['price'].sum() + min(unused_actions_list.iloc, key=lambda x: x['price'])['price']
    except ValueError:
        next_min = max_invest_price + 1
    if actions_list['price'].sum() == max_invest_price:
        return [actions_list]
    elif next_min > max_invest_price:
        return []
    else:
        action = unused_actions_list.iloc[0]
        unused_actions_list_copy = unused_actions_list.copy()
        unused_actions_list_copy.drop([action.name], axis=0, inplace=True)
        if actions_list['price'].sum() + action['price'] <= max_invest_price:
            return [
                *building_invest_actions_list(
                    pd.concat(
                        [
                            actions_list,
                            action.to_frame().transpose()
                        ],
                        ignore_index=True
                    ),
                    unused_actions_list_copy,
                    max_invest_price
                ),
                *building_invest_actions_list(
                    actions_list,
                    unused_actions_list_copy,
                    max_invest_price
                )
            ]
        else:
            return building_invest_actions_list(
                actions_list,
                unused_actions_list_copy,
                max_invest_price
            )


def test_opti_two(actions_list: pd.DataFrame, max_invest_price: float = 500):
    """
    only test function
    :param actions_list:
    :param max_invest_price:
    :return:
    """
    unused_actions_list = actions_list.copy()
    invest_action_list = pd.DataFrame({'price': []})
    unused_actions_list = calc.calc_profits(unused_actions_list).sort_values(by=['profits'])
    invest_action_lists = []
    while invest_action_list['price'].sum() < max_invest_price:
        action = unused_actions_list.iloc[0]
        if invest_action_list['price'].sum() + action['price'] == max_invest_price:
            invest_action_lists.append(invest_action_list)
