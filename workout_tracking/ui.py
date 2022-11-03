from typing import Protocol

from person import Person


class UI(Protocol):
    def display_logo(self) -> None:
        raise NotImplementedError()

    def read_workouts_info(self) -> str:
        raise NotImplementedError()

    def show_error(self, msg: str) -> None:
        raise NotImplementedError()

    def display_success_msg(self) -> None:
        raise NotImplementedError()
    
    def display_no_exercise_msg(self) -> None:
        raise NotImplementedError()

    def read_gender(self) -> str:
        raise NotImplementedError()

    def read_weight(self) -> float:
        raise NotImplementedError()

    def read_height(self) -> float:
        raise NotImplementedError()

    def read_age(self) -> int:
        raise NotImplementedError()

    def ask_for_personal_data(self) -> Person:
        raise NotImplementedError()
