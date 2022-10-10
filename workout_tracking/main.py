from datetime import datetime

from models import Exercise, Workout


def show_error(msg: str) -> None:
    print(f"\033[1;31mError: {msg}\033[1m")


def main() -> None:
    user_input = input("Tell me what exercises you did today:").strip()

    try:
        exercise_data = Exercise.extract_data_from_text(user_input)
    except Exception as err:
        show_error("Unable to extract workout data from your description.\n"
                   f"{err}")
    else:
        if len(exercise_data) > 0:
            today = datetime.now()

            for exercise in exercise_data:
                try:
                    workout = Workout(
                        date=today.strftime("%d/%m/%Y"),
                        time=today.strftime("%H:%M:%S"),
                        exercise=Exercise.parse_obj(exercise)
                    )

                    Workout.save_to_spreadsheet(workout)
                except Exception as err:
                    show_error(f"Could not save workout to worksheet.\n"
                               f"{err}")
                else:
                    print(f"Workout saved successfully.\n{workout}")


if __name__ == "__main__":
    main()
