import time

import pandas as pd

import data
import bruteforce

for i in range(10):
    tt = time.time()
    data.display_actions_list(bruteforce.get_best_invest_action_list(data.actions, (i + 1) * 50))
    print(time.time() - tt)

