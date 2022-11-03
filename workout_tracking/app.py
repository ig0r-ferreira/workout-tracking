from datetime import datetime
from enum import Enum, auto
from typing import Any

from nutrition_api import NutritionAPI
from person import Person
from sheet_api import SheetAPI
from ui import UI


class MenuOptions(Enum):
    REGISTER_WORKOUTS = auto()
    SHOW_PERSONAL_DATA = auto()
    CHANGE_PERSONAL_DATA = auto()
    EXIT = auto()


class WorkoutTrackingApp:
    def __init__(
        self,
        ui: UI,
        nutrition_api: NutritionAPI,
        sheet_api: SheetAPI,
        today: datetime,
        personal_data: Person | None
    ) -> None:
        self.ui = ui
        self.nutrition_api = nutrition_api
        self.sheet_api = sheet_api
        self.today = today
        self.personal_data = personal_data

    def save_workouts_in_spreadsheet(
        self,
        workout_data: list[dict[str, Any]]
    ) -> None:
        try:
            self.sheet_api.add_rows_in_sheet(
                sheet_name="workouts",
                obj_name="workout",
                rows=workout_data
            )
        except Exception as exc:
            self.ui.show_error(str(exc))
        else:
            self.ui.display_success_msg()

    def register_workouts(self) -> None:
        workouts_info = self.ui.read_workouts_info()

        exercise_data = self.nutrition_api.get_exercises_from_text(
            text=workouts_info,
            personal_data=self.personal_data.dict()
        )

        if not exercise_data:
            self.ui.display_no_exercise_msg()
            return

        workout_data = [
            {
                "date": f"{self.today:%d/%m/%Y}",
                "time": f"{self.today:%H:%M:%S}",
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
            for exercise in exercise_data
        ]

        self.save_workouts_in_spreadsheet(workout_data)

    def show_personal_data(self) -> None:
        self.ui.display_personal_data(self.personal_data)

    def change_personal_data(self) -> None:
        self.personal_data = self.ui.ask_for_personal_data()

    def run(self) -> None:
        while True:
            self.ui.display_logo()
            
            menu_option = MenuOptions.REGISTER_WORKOUTS

            if self.personal_data is None:
                self.personal_data = self.ui.ask_for_personal_data()
            else:
                self.ui.display_menu(MenuOptions)
                menu_option = self.ui.read_menu_option(MenuOptions)

            match menu_option:
                case MenuOptions.REGISTER_WORKOUTS:
                    self.register_workouts()
                case MenuOptions.SHOW_PERSONAL_DATA:
                    self.show_personal_data()
                case MenuOptions.CHANGE_PERSONAL_DATA:
                    self.change_personal_data()
                case MenuOptions.EXIT:
                    return
                case _:
                    self.ui.show_error("Option not found in the menu.")
