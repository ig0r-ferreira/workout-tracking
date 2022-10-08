from datetime import datetime
from models import Exercise, Workout


def main() -> None:
    user_description = input("Tell me what exercises you did today: ").strip()
    exercise_data = Exercise.extract_data_from_text(user_description)

    if len(exercise_data) > 0:
        today = datetime.now()

        for exercise in exercise_data:
            workout = Workout(
                date=today.strftime("%d/%m/%Y"),
                time=today.strftime("%H:%M:%S"),
                exercise=Exercise.parse_obj(exercise)
            )

            Workout.save_to_spreadsheet(workout)


if __name__ == "__main__":
    main()
