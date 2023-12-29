from typing import Any
import json, os, tools


class DB:
    def __init__(self, path: str = "db.json") -> None:
        self.path = path
        self.data: dict[str, Any] = {"leaderboards": {}, "msg_history": "", "polls": {}}

        if not os.path.exists(self.path):
            with open(self.path, "w") as fp:
                json.dump(self.data, fp)

    def save(self) -> None:
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def load(self) -> None:
        with open(self.path) as fp:
            self.data = json.load(fp)

    def add_win(self, leaderboard: str, player_id: int) -> None:
        self.load()

        if not self.data["leaderboards"].get(leaderboard):
            self.data["leaderboards"][leaderboard] = {}

        if not self.data["leaderboards"][leaderboard].get(str(player_id)):
            self.data["leaderboards"][leaderboard][str(player_id)] = 0

        self.data["leaderboards"][leaderboard][str(player_id)] += 1

        self.save()

    def get_leaderboard(self, leaderboard: str) -> dict[str, int]:
        self.load()

        if not self.data["leaderboards"].get(leaderboard):
            return {}

        return dict(
            sorted(
                self.data["leaderboards"][leaderboard].items(),
                key=(lambda item: item[1]),
                reverse=True,
            )
        )

    def set_msg_history(self, history: str):
        self.load()
        self.data["msg_history"] = history
        self.save()

    def get_msg_history(self) -> str:
        self.load()
        return self.data.get("msg_history", "")

    def add_msg(self, msg: str):
        self.load()

        if not self.data.get("msg_history"):
            self.data["msg_history"] = msg
            return

        self.data["msg_history"] += f"\n{msg}"

        self.save()

    def clear_msg_history(self):
        self.load()
        self.data["msg_history"] = ""
        self.save()

    def create_poll(self, options: list[int]) -> str:
        self.load()
        id = tools.random_id()
        self.data["polls"][id] = {"options": options, "votes": {}}
        self.save()
        return id

    def set_vote(self, poll_id: str, user_id: int, option: int):
        self.load()
        self.data["polls"][poll_id]["votes"][str(user_id)] = option
        self.save()

    def get_votes(self, poll_id: str) -> dict[str, int]:
        self.load()
        votes = {}

        for option in self.data["polls"][poll_id]["options"]:
            votes[str(option)] = 0

        for vote in self.data["polls"][poll_id]["votes"].values():
            votes[vote] += 1

        return votes

    def remove_vote(self, poll_id: str, user_id: int):
        self.load()

        try:
            del self.data["polls"][poll_id]["votes"][str(user_id)]
        except:
            pass

        self.save()
