import os
import logging
import datetime as dt
import time

# current_month=dt.datetime.now().month
# LOG_FILE = os.getcwd() + "/logs"
# if not os.path.exists(LOG_FILE):
#     os.makedirs(LOG_FILE)
# LOG_FILE = LOG_FILE + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d') + ".log"
# logFormatter = logging.Formatter("%(levelname)s %(asctime)s %(processName)s %(message)s")
# fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
# fileHandler.setFormatter(logFormatter)
# rootLogger = logging.getLogger()
# rootLogger.addHandler(fileHandler)
# rootLogger.setLevel(logging.INFO)
#
# print(os.getcwd())
log_folder = os.getcwd() + "/logs"
month_log_folder = log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m')
LOG_FILE = month_log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d') + ".log"
logFormatter = logging.Formatter("%(asctime)s %(message)s",
                                 "%Y-%m-%d")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

# def configure_day_log():
#     global LOG_FILE
#     month_log_folder = log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m')
#     if not os.path.exists(month_log_folder):
#         os.makedirs(month_log_folder)
#     LOG_FILE = month_log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d') + ".log"
#     fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
#     fileHandler.setFormatter(logFormatter)
#     rootLogger.addHandler(fileHandler)


def configure_day_log():
    global LOG_FILE
    global month_log_folder
    month_log_folder = log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m')
    if not os.path.exists(month_log_folder):
        os.makedirs(month_log_folder)
    LOG_FILE = month_log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d') + ".log"
    for hdlr in rootLogger.handlers[:]:  # remove the existing file handlers
        if isinstance(hdlr, logging.FileHandler):
            rootLogger.removeHandler(hdlr)
    fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)  # set the new handler

configure_day_log()

logging.info(dt.datetime.now().strftime('%H:%M:%S')+" Программа запущена")
