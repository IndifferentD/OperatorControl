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

log_folder = os.getcwd() + "/logs"
logFormatter = logging.Formatter("%(asctime)s %(message)s",
                                 "%Y-%m-%d")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

def configure_day_log():
    global LOG_FILE
    month_log_folder = log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m')
    if not os.path.exists(month_log_folder):
        os.makedirs(month_log_folder)
    LOG_FILE = month_log_folder + "/" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d') + ".log"
    fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
    fileHandler.setFormatter(logFormatter)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(fileHandler)
    rootLogger.setLevel(logging.INFO)

configure_day_log()

# logging.info("testing out the logging functionality")
