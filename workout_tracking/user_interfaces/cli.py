def read_float(msg: str) -> float:
    while True:
        try:
            value = float(input(msg))
        except ValueError:
            raise ValueError("The value entered is not a number.")
        else:
            return value


class CLI:
    @staticmethod
    def read_workouts_description() -> str:
        return input("Tell me what exercises you did today: ").strip()

    @staticmethod
    def show_error(msg: str) -> None:
        print(f"\033[1;31mError: {msg}\033[m")

    @staticmethod
    def display_success_msg(msg: str) -> None:
        print(msg)

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
