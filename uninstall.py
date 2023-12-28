#!/bin/python3
import os, logger, getpass

user = getpass.getuser()
cwd = os.getcwd()

logger.info("deleting bot repo...")

if os.system(f"rm -r '{repr(cwd)}'") != 0:
    logger.error("failed!")
    exit(1)

logger.info("disabling and stopping bot service...")

if os.system("sudo systemctl disable --now CranberryBot") != 0:
    logger.error("failed!")
    exit(1)

logger.info("deleting bot service...")

if os.system("sudo rm /lib/systemd/system/CranberryBot.service") != 0:
    logger.error("failed!")
    exit(1)

logger.info("done")
