from os.path import isfile, join
from os import getcwd

import pandas as pd

import views
from .checkers import check_menu, check_form
from .dataprocessing.inoutdata import DataLoader
from .dataprocessing.calc import actions_list_report
from .dataprocessing import Bruteforce, OptimisedBruteforce, Optimised, BestActionsListInterface


class Simulations(DataLoader):

    @staticmethod
    def get_algorithm(view: views.ViewsInterface) -> tuple[str, type]:
        options = [
            (
                'Bruteforce',
                Bruteforce
            ),
            (
                'Bruteforce optimiser',
                OptimisedBruteforce
            ),
            (
                'Algorithm optimisé',
                Optimised
            )
        ]

        return options[check_menu(
            view=view,
            items=[option[0] for option in options],
            header='Avec quel algorithm voulez vous effectuer la simulation ?'
        )]

    @classmethod
    def load_data(cls, view: views.ViewsInterface):
        options = [
            (
                'Donnée de test',
                cls.load_test_data,
                {}
            ),
            (
                'Charger des données depuis un fichier (csv)',
                cls.load_data_from_file,
                {
                    'view': view
                }
            )
        ]
        option_key = check_menu(
            view=view,
            items=[option[0] for option in options],
            header='Avec quelle données voulez vous effectuer la simulation ?'
        )
        return options[option_key][1](
            **options[option_key][2]
        )


    @classmethod
    def load_data_from_csv_file(cls, view: views.ViewsInterface) -> pd.DataFrame | None:
        form = {
            'file_path': (
                'Emplacement du fichier csv : ',
                lambda path: isfile(join(getcwd(), path)) and path[-4:] == '.csv',
                ' est chemin de fichier csv incorect'
            )
        }
        file_path = check_form(
            view=view,
            fields=form
        )['file_path']
        return cls.load_csv_file(file_path=file_path)

    @classmethod
    def load_data_from_file(cls, view: views.ViewsInterface) -> pd.DataFrame | None:
        data = cls.load_data_from_csv_file(view=view)
        columns_names = cls.get_column_names(view=view)
        columns_renames = {}
        for key, val in columns_names.items():
            if key != val:
                columns_renames[val] = key
        return cls.rename_data_frame_column(data, columns_renames)

    @classmethod
    def run(cls, view: views.ViewsInterface):
        max_invest = 500
        algorithm = cls.get_algorithm(view=view)
        data = cls.load_data(view=view)
        view.display_data_frame(
            data_frame=data.sort_values(by=['efficiency'], ascending=False).head()
        )
        actions_list = algorithm[1].get_best_actions_list(
            actions_list=data,
            invest_max=max_invest
        )
        view.display_data_frame(
            data_frame=actions_list
        )
        view.display_data_frame(
            data_frame=actions_list_report(actions_list, max_invest)
        )

    @classmethod
    def get_column_names(cls, view: views.ViewsInterface):
        form = {
            'name': (
                'Nom de la colonne du nom des actions : ',
                lambda name: name.isalpha(),
                ' n\'est pas un nom de colonne valide'
            ),
            'price': (
                'Nom de la colonne du prix des actions : ',
                lambda name: name.isalpha(),
                ' n\'est pas un nom de colonne valide'
            ),
            'efficiency': (
                'Nom de la colonne du rendement des actions : ',
                lambda name: name.isalpha(),
                ' n\'est pas un nom de colonne valide'
            )
        }
        return check_form(
            view=view,
            fields=form
        )

    @classmethod
    def rename_data_frame_column(cls, data_frame: pd.DataFrame, columns_renames) -> pd.DataFrame:
        return data_frame.rename(columns=columns_renames)
