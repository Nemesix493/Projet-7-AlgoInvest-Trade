import pandas as pd

from . import calc
from .bestactionslistinterface import BestActionsListInterface


class OptimisedBruteforce(BestActionsListInterface):
    @classmethod
    def get_best_actions_list(cls, actions_list: pd.DataFrame, invest_max: float = 500) -> pd.DataFrame:
        return max(
            cls.building_invest_actions_list(pd.DataFrame({'price': []}), actions_list, invest_max),
            key=calc.action_list_profit
        )

    @classmethod
    def building_invest_actions_list(cls, actions_list: pd.DataFrame, unused_actions_list: pd.DataFrame,
                                     invest_max: float = 500) -> list[pd.DataFrame]:
        try:
            next_min = actions_list['price'].sum() + min(unused_actions_list.iloc, key=lambda x: x['price'])['price']
        except ValueError:
            next_min = invest_max + 1
        if actions_list['price'].sum() == invest_max:
            return [actions_list]
        elif next_min > invest_max:
            return []
        else:
            action = unused_actions_list.iloc[0]
            unused_actions_list_copy = unused_actions_list.copy()
            unused_actions_list_copy.drop([action.name], axis=0, inplace=True)
            if actions_list['price'].sum() + action['price'] <= invest_max:
                return [
                    *cls.building_invest_actions_list(
                        pd.concat(
                            [
                                actions_list,
                                action.to_frame().transpose()
                            ],
                            ignore_index=True
                        ),
                        unused_actions_list_copy,
                        invest_max
                    ),
                    *cls.building_invest_actions_list(
                        actions_list,
                        unused_actions_list_copy,
                        invest_max
                    )
                ]
            else:
                return cls.building_invest_actions_list(
                    actions_list,
                    unused_actions_list_copy,
                    invest_max
                )