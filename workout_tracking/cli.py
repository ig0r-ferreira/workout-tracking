from enum import Enum, EnumMeta

from person import Person

LOGO = r"""        
___       __            ______              _____     ________                   ______ _____                
__ |     / /_______________  /___________  ___  /_    ___  __/____________ _________  /____(_)_____________ _
__ | /| / /_  __ \_  ___/_  //_/  __ \  / / /  __/    __  /  __  ___/  __ `/  ___/_  //_/_  /__  __ \_  __ `/
__ |/ |/ / / /_/ /  /   _  ,<  / /_/ / /_/ // /_      _  /   _  /   / /_/ // /__ _  ,<  _  / _  / / /  /_/ / 
____/|__/  \____//_/    /_/|_| \____/\__,_/ \__/      /_/    /_/    \__,_/ \___/ /_/|_| /_/  /_/ /_/_\__, /  
                                                                                                    /____/   
"""  # noqa: E501, W291


def read_float(msg: str) -> float:
    while True:
        try:
            value = float(input(msg))
        except ValueError as exc:
            raise ValueError("The value entered is not a number.") from exc
        else:
            return value


class CLI:
    @staticmethod
    def display_logo() -> None:
        print(LOGO)

    def display_menu(self, menu: EnumMeta) -> None:
        for option in menu:
            print(f"{option.value} - {option.name.replace('_', ' ')}")

    def read_menu_option(self, menu: EnumMeta) -> Enum:
        print()
        while True:
            user_option = input("Which option do you want: ")
            try:
                return menu(int(user_option))
            except ValueError:
                self.show_error(
                    "Invalid option. Select one of the options "
                    "available from the menu."
                )

    def read_workouts_info(self) -> str:
        while True:
            workouts_info = input(
                "Tell me what exercises you did today: "
            ).strip()

            if workouts_info:
                return workouts_info

            self.show_error("Empty description. Try again!")

    @staticmethod
    def show_error(msg: str) -> None:
        print(f"\033[1;31mError: {msg}\033[m")

    @staticmethod
    def display_success_msg() -> None:
        print("Data successfully saved to the spreadsheet.")

    @staticmethod
    def display_no_exercise_msg() -> None:
        print("No exercises were identified in its description.")

    @staticmethod
    def read_gender() -> str:
        return input("Enter your gender [m/f]: ").lower()

    @staticmethod
    def read_weight() -> float:
        return read_float("Enter your weight(kg): ")

    @staticmethod
    def read_height() -> float:
        return read_float("Enter your height(cm): ")

    @staticmethod
    def read_age() -> int:
        return int(read_float("Enter your age: "))

    def ask_for_personal_data(self) -> Person:
        while True:
            try:
                person = Person(
                    gender=self.read_gender(),
                    weight_kg=self.read_weight(),
                    height_cm=self.read_height(),
                    age=self.read_age()
                )
            except Exception as exc:
                self.show_error(str(exc))
            else:
                return person

    @staticmethod
    def display_personal_data(person: Person) -> None:
        for key, value in person:
            print(f"{key.upper()}: {value}")
