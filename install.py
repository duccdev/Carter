#!/bin/python3
import os, logger, getpass

if getpass.getuser() != "root":
    logger.error("please re-run with sudo!")
    exit(1)

user = input("user to install as [root]: ").strip() or "root"
cwd = os.getcwd()

logger.info("setting up venv...")
os.system(f'su {user} -c "python3 -m venv .venv"')

logger.info("installing dependencies...")
os.system(
    f'su {user} -c "source .venv/bin/activate && .venv/bin/pip3 install -U -r requirements.txt"'
)

logger.info("installing systemd service...")

with open("CranberryBot.service") as fp:
    service = fp.read()

service = service.replace("USER_GOES_HERE", user).replace(
    "WORKING_DIRECTORY_GOES_HERE", cwd
)

try:
    with open("/lib/systemd/system/CranberryBot.service", "w") as fp:
        fp.write(service)
except Exception as e:
    logger.error(str(e))
    exit(1)

logger.info("enabling and starting service...")

if os.system("sudo systemctl enable --now CranberryBot") != 0:
    logger.error("failed!")
    exit(1)

logger.info("done")
