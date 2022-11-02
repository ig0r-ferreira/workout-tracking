from datetime import datetime

from app import WorkoutTrackingApp
from cli import CLI
from nutrition_api import NutritionixAPI
from person_controller import load_personal_data, save_personal_data
from sheet_api import SheetyAPI


def main() -> None:
    cli = CLI()

    app = WorkoutTrackingApp(
        ui=cli,
        nutrition_api=NutritionixAPI(),
        sheet_api=SheetyAPI(),
        today=datetime.today(),
        personal_data=load_personal_data()
    )
    app.run()
    save_personal_data(app.personal_data)


if __name__ == "__main__":
    main()
