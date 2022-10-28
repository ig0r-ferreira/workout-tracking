from typing import Any, Protocol

import requests

from workout_tracking.settings import SheetAPISettings


Row = dict[str, Any]


class SheetAPI(Protocol):
    def add_rows_in_sheet(
        self, sheet_name: str, obj_name: str, rows: list[Row]
    ) -> None:
        raise NotImplementedError()


class SheetyAPI(SheetAPISettings):
    def add_rows_in_sheet(
            self, sheet_name: str, obj_name: str, rows: list[Row]
    ) -> None:
        for row in rows:
            requests.post(
                url=f"{self.ENDPOINT}{sheet_name}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.KEY_AUTH
                },
                json={
                    obj_name: row
                }
            )
