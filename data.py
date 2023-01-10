import pandas as pd


actions = {
    'name': [],
    'price': [],
    'moneyReturnRate': []
}
actions = pd.DataFrame(actions)


def add_actions_to_actions_list(actions_list: pd.DataFrame, name: str, price: int,
                                money_return_rate: int) -> pd.DataFrame:
    return pd.concat(
        [
            actions_list,
            pd.DataFrame({
                'name': [name],
                'price': [price],
                'moneyReturnRate': [money_return_rate]
            })
        ],
        ignore_index=True
    )


with open('actions.txt', 'r') as data:
    for line in data:
        current_action = line.replace('%', '').replace(' ', '').replace('\n', '').split('\t')
        actions = add_actions_to_actions_list(
            actions_list=actions,
            name=current_action[0],
            price=int(current_action[1]),
            money_return_rate=int(current_action[2])
        )