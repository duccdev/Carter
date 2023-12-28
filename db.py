from typing import Any
import json
import os
from threading import Timer


class DB:
    def __init__(self, path: str = "db.json") -> None:
        self.path = path
        self.data: dict[str, Any] = {"leaderboards": {}}

        if not os.path.exists(self.path):
            with open(self.path, "w") as fp:
                json.dump(self.data, fp)

        def clean_up():
            self.load()
            self.clear_msg_history()
            self.save()
            Timer(60 * 10, clean_up)

        Timer(60 * 10, clean_up)

    def save(self) -> None:
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def load(self) -> None:
        with open(self.path) as fp:
            self.data = json.load(fp)

    def add_win(self, leaderboard: str, player_id: int) -> None:
        if not self.data["leaderboards"].get(leaderboard):
            self.data["leaderboards"][leaderboard] = {}

        if not self.data["leaderboards"][leaderboard].get(str(player_id)):
            self.data["leaderboards"][leaderboard][str(player_id)] = 0

        self.data["leaderboards"][leaderboard][str(player_id)] += 1

    def get_leaderboard(self, leaderboard: str) -> dict[str, int]:
        if not self.data["leaderboards"].get(leaderboard):
            return {}

        return dict(
            sorted(
                self.data["leaderboards"][leaderboard].items(),
                key=(lambda item: item[1]),
                reverse=True,
            )
        )

    def get_msg_history(self) -> str:
        if not self.data.get("msg_history"):
            return ""

        return self.data["msg_history"]

    def set_msg_history(self, history: str):
        self.data["msg_history"] = history

    def add_msg(self, msg: str):
        if not self.data.get("msg_history"):
            self.data["msg_history"] = msg
            return

        self.data["msg_history"] += f"\n{msg}"

    def clear_msg_history(self):
        del self.data["msg_history"]
