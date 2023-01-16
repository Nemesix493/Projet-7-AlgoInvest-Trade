import abc

import pandas as pd


class BestActionsListInterface(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def get_best_actions_list(cls, actions_list: pd.DataFrame, invest_max: float = 500) -> pd.DataFrame:
        pass
