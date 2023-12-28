#!/bin/python3
import os, logger

user = input("User to install as [root]: ").strip() or "root"
cwd = os.getcwd()

logger.info("installing systemd service...")

with open("CranberryBot.service") as fp:
    service = fp.read()

service.replace("USER_GOES_HERE", user)
service.replace("WORKING_DIRECTORY_GOES_HERE", cwd)

try:
    with open("/lib/systemd/system/CranberryBot.service", "w") as fp:
        fp.write(service)
except Exception as e:
    logger.error(str(e))
    exit(1)

logger.info("done")
