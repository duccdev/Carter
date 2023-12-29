from subprocess import run


def get_live_commit() -> tuple[str, str]:
    return (
        run(
            ["git", "log", "-n1", '--format="%h"'],
            capture_output=True,
            text=True,
        ).stdout.strip()[1:-1],
        run(
            ["git", "log", "-n1", '--format="%H"'],
            capture_output=True,
            text=True,
        ).stdout.strip()[1:-1],
    )
