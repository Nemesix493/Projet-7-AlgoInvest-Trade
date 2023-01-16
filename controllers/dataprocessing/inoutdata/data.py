from os import path

import pandas as pd


class DataLoader:
    @staticmethod
    def load_test_data():
        return pd.read_csv(
            path.join(path.dirname(__file__), 'exemple.csv')
        )

    @staticmethod
    def load_csv_file(file_path: str):
        return pd.read_csv(file_path)
