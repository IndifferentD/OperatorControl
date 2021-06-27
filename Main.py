from threading import Timer
from datetime import datetime, time

import time as t

import schedule
import report
import GUI

from threading import Thread
# import string
# import os
# import time as t
# import gc
# from pympler.tracker import SummaryTracker
#
# tracker = SummaryTracker()
import cfg


# gc.enable()
# gc.set_debug(1)

# TODO: Протестировать скелдью
def start_control():
    if GUI.current_user != ('admin' or None):
        GUI.generate_timer = GUI.RepeatableTimer(GUI.generate_appear_interval(), GUI.generate_win_pos_and_timer, ())
        GUI.generate_timer.start()


def end_control():
    # TODO: если проверочное окно открыто - закрыть (с записью?)
    print('Контроль прекращен')
    GUI.stop_timers()


def init_jobs():
    schedule.clear()
    schedule.every().day.at(cfg.config.read()['TimeSettings']['shiftstart']).do(start_control)
    schedule.every().day.at(cfg.config.read()['TimeSettings']['ReportSendTime']).do(report.send_report)
    schedule.every().day.at(cfg.config.read()['TimeSettings']['shiftend']).do(end_control)


def scheldue_job_pender():
    while True:
        schedule.run_pending()
        t.sleep(1)


init_jobs()

ScldReportThread = Thread(target=scheldue_job_pender, )
ScldReportThread.daemon=True
ScldReportThread.start()
