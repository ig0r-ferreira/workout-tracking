from dataclasses import dataclass
from datetime import datetime

from nutrition_api import NutritionAPI
from person import Person
from sheet_api import SheetAPI
from ui import UI


@dataclass
class WorkoutTrackingApp:
    ui: UI
    nutrition_api: NutritionAPI
    sheet_api: SheetAPI
    today: datetime
    personal_data: Person | None

    def run(self) -> None:
        self.ui.display_logo()

        if self.personal_data is None:
            self.personal_data = self.ui.ask_for_personal_data()

        description = self.ui.read_workouts_description()

        exercise_data = self.nutrition_api.get_exercises_from_text(
            text=description, **self.personal_data.dict()
        )

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

        self.sheet_api.add_rows_in_sheet(
            sheet_name="workouts",
            obj_name="workout",
            rows=workout_data
        )
        self.ui.display_success_msg(
            "Data successfully saved to the spreadsheet."
        )
