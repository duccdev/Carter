import json
import os


class DB:
    def __init__(self, path: str = "db.json") -> None:
        self._path = path
        self._data = {"leaderboards": {}}

        if not os.path.exists(self._path):
            with open(self._path, "w") as fp:
                json.dump(self._data, fp)

    def save(self) -> None:
        with open(self._path, "w") as fp:
            json.dump(self._data, fp)

    def load(self) -> None:
        with open(self._path) as fp:
            self._data = json.load(fp)

    def add_win(self, leaderboard: str, player_id: int) -> None:
        if not self._data["leaderboards"].get(leaderboard):
            self._data["leaderboards"][leaderboard] = {}

        self._data["leaderboards"][leaderboard][str(player_id)] += 1

    def get_leaderboard(self, leaderboard: str) -> dict[str, int]:
        if not self._data["leaderboards"].get(leaderboard):
            return {}

        return dict(
            sorted(
                self._data["leaderboards"][leaderboard].items(),
                key=(lambda item: item[1]),
                reverse=True,
            )
        )
