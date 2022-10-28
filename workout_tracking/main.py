from datetime import datetime


from app import WorkoutTrackingApp
from models.person import Person
from settings import load_personal_data, save_personal_data
from user_interfaces.cli import CLI
from user_interfaces.ui import UI
from utils.nutrition_api import NutritionixAPI
from utils.sheet_api import SheetyAPI


def ask_for_personal_data(ui: UI) -> Person:
    while True:
        try:
            person = Person(
                gender=ui.read_gender(),
                weight_kg=ui.read_weight(),
                height_cm=ui.read_height(),
                age=ui.read_age()
            )
        except Exception as error:
            ui.show_error(str(error))
        else:
            return person


def main() -> None:
    cli = CLI()

    personal_data = load_personal_data() or ask_for_personal_data(cli)

    app = WorkoutTrackingApp(
        ui=cli,
        nutrition_api=NutritionixAPI(),
        sheet_api=SheetyAPI(),
        today=datetime.today(),
        personal_data=personal_data
    )
    app.run()
    save_personal_data(app.personal_data)


if __name__ == "__main__":
    main()
