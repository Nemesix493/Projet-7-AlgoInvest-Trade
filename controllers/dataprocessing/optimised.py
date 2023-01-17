import math

import pandas as pd

from .bestactionslistinterface import BestActionsListInterface
from .bruteforce import Bruteforce
from . import calc


class Optimised(BestActionsListInterface):
    @classmethod
    def get_best_actions_list(cls, actions_list: pd.DataFrame, invest_max: float = 500):
        """
        only test function
        :param actions_list:
        :param invest_max:
        :return:
        """
        to_use_actions_list = actions_list.sort_values(by=['efficiency'], ascending=False)
        for action in to_use_actions_list.iloc:
            if action['price'] > invest_max:
                to_use_actions_list = to_use_actions_list.drop(index=action.name)
        length = 1
        while to_use_actions_list.head(length)['price'].sum() < 2 * invest_max and length < len(to_use_actions_list):
            length += 1
        to_use_actions_list = to_use_actions_list.head(length)
        number_actions = 1
        while to_use_actions_list.head(number_actions)['price'].sum() < invest_max:
            number_actions += 1
        number_actions -= 1
        invest_action_lists = [to_use_actions_list.head(number_actions)]
        length_limit = number_actions * math.log(math.factorial(number_actions))
        head = number_actions
        tail = length - number_actions - 1
        while len(invest_action_lists) < length_limit and head > 1:
            invest_action_lists += Bruteforce.building_invest_actions_list(
                actions_list=to_use_actions_list.head(head),
                unused_actions_list=to_use_actions_list.tail(tail),
                invest_max=invest_max
            )
            head -= 1
            tail += 1
        return max(invest_action_lists, key=calc.action_list_profit)

