from views import ViewsInterface
from .checkers import check_menu
from .simulations import Simulations


def main_menu(view: ViewsInterface):
    options = [
        (
            'Effectuer une simulation',
            Simulations.run,
            {
                'view': view
            }
        ),
        (
            'Quitter',
            quit,
            {}
        )
    ]
    while True:
        option_index = check_menu(
            view=view,
            items=[option[0] for option in options],
            title='Menu principal'
        )
        options[option_index][1](**options[option_index][2])
