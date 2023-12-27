import os


def ping() -> str:
    os.system("ping 1.1.1.1 -c 1 > /tmp/ping")

    with open("/tmp/ping") as fp:
        ping = fp.read().splitlines()[1]
        ping = ping[(ping.find("time=") + 5) :]

    os.remove("/tmp/ping")

    return ping
