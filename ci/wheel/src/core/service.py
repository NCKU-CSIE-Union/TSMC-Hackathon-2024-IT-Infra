import os
import logging


def create_runner(service):
    # create `./tasks/service` file

    logger = logging.getLogger(service)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    logger.info(f"Creating task: {service}")

    if not os.path.exists("./tasks/"):
        os.mkdir("./tasks/")

    if not os.path.exists(f"./tasks/{service}"):
        with open(f"./tasks/{service}", "w") as f:
            f.write("")

    logger.info(f"Task created: {service}")
