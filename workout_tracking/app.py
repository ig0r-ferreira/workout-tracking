from dataclasses import dataclass
from datetime import datetime
from typing import Any

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

    def register_workouts(self, workout_data: list[dict[str, Any]]) -> None:
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

    def run(self) -> None:
        self.ui.display_logo()

        if self.personal_data is None:
            self.personal_data = self.ui.ask_for_personal_data()

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

        self.register_workouts(workout_data)
