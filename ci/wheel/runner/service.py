import os
import subprocess
import logging
import time
import yaml


def check_new_task():
    # if ./tasks/* exists
    # using `ls ./tasks`
    # then run the task

    ls_output = subprocess.check_output(["ls", "./tasks"])
    ls_output = ls_output.decode("utf-8")

    if len(ls_output) > 0:
        tasks = ls_output.split("\n")
        for task in tasks:
            if len(task) > 0:
                consumer_task(task)


def get_logger(task_name):
    logger = logging.getLogger(task_name)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f"./logs/{task_name}.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


def get_global_logger():
    logger = logging.getLogger("global")
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("./logs/global.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger


def run_yaml_task(yaml_path, logger):
    with open(yaml_path) as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)

    if yaml_file is None:
        logger.error(f"Unable to read yaml file: {yaml_path}")
        return

    logger.info(f"Running yaml: {yaml_path}")
    logger.info(f"Task: {yaml_file.get('name')}")

    # run the task
    steps = yaml_file.get("steps")
    for step in steps:
        name = step.get("name")
        commands = step.get("commands")

        logger.info(f"Step: {name}")

        for command in commands:
            logger.info(f"Running command: {command}")

            # run the command
            try:
                output = subprocess.check_output(command.split(" "))
                output = output.decode("utf-8")
                logger.info(f"Output:\n{output}")
            except Exception as e:
                logger.error(f"Error: {e}")


def consumer_task(task_name):
    global_logger = get_global_logger()
    global_logger.info(f"Found new task: {task_name}")
    logger = get_logger(task_name)

    # check make sure task_name is a valid task
    if os.path.isfile(f"./yaml/{task_name}.yaml"):
        # YYYY-MM-DD HH:MM:SS
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"========= RUNNER START : {now} =========")

        # run the task
        run_yaml_task(f"./yaml/{task_name}.yaml", logger)

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"========= RUNNER DONE : {now} =========")

    # remove the task
    os.remove(f"./tasks/{task_name}")
    global_logger.info(f"Removed task: {task_name}")
