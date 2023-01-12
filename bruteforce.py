import calc

import pandas as pd


def building_invest_actions_list(actions_list: pd.DataFrame, unused_actions_list: pd.DataFrame,
                                 max_invest_price: float = 500) -> list[pd.DataFrame]:
    try:
        next_min = actions_list['price'].sum() + min(unused_actions_list.iloc, key=lambda x: x['price'])['price']
    except ValueError:
        return [actions_list]
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


def get_best_invest_action_list(actions_list: pd.DataFrame, max_invest_price: float = 500) -> pd.DataFrame:
    invest_actions_list = building_invest_actions_list(
        pd.DataFrame({'price': []}),
        actions_list,
        max_invest_price
    )
    return max(invest_actions_list, key=calc.action_list_balance)
