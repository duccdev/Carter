#!/usr/bin/env python3
import os, logger, getpass

user = getpass.getuser()
cwd = os.getcwd()

logger.info("setting up venv...")

if os.system("python3 -m venv .venv") != 0:
    logger.error("failed!")

logger.info("installing dependencies...")

if (
    os.system(
        'bash -c "source .venv/bin/activate && .venv/bin/pip3 install -U -r requirements.txt && prisma db push && prisma generate"'
    )
    != 0
):
    logger.error("failed!")
    exit(1)

logger.info("installing systemd service...")

with open("Carter.service") as fp:
    service = fp.read()

service = service.replace("USER_GOES_HERE", user).replace(
    "WORKING_DIRECTORY_GOES_HERE", cwd
)

try:
    with open("/tmp/Carter.service", "w") as fp:
        fp.write(service)
except Exception as e:
    logger.error(str(e))
    exit(1)

if os.system("sudo mv /tmp/Carter.service /lib/systemd/system") != 0:
    logger.error("failed!")
    exit(1)

logger.info("enabling and starting service...")

if os.system("sudo systemctl enable --now Carter") != 0:
    logger.error("failed!")
    exit(1)

logger.info("done")
