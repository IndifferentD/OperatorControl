
from threading import Timer
from datetime import datetime, time

import time as t
import logg
import schedule
import snd_mail
import GUI

from threading import Thread
# import string
# import os
# import time as t
# import gc
# from pympler.tracker import SummaryTracker
#
# tracker = SummaryTracker()

# gc.enable()
# gc.set_debug(1)

## Настройки
Control_time_start_set = '09:00'  # Начало тестируемого интервала в день начала смены
Control_time_start = datetime.strptime(Control_time_start_set, '%H:%M').time()
Control_time_end_set = '07:00'  # Конец тестируемого интервала на следующий день
Control_time_end = datetime.strptime(Control_time_end_set, '%H:%M').time()


snd_rpt_hour = 8  # час отправки отчета
snd_rpt_minute = 0  # минуты отправки отчета
snd_rpt_time = time(snd_rpt_hour, snd_rpt_minute)

def send_report():
    snd_mail.send_mail('test', ['mozgunov.gs@gmail.com'], 'test', 'test', files=[logg.LOG_FILE],
                       server="smtp.yandex.ru", port=465, username='IndifferentD@yandex.ru', password='',
                       use_tls=True)


def start_control():
    logg.configure_day_log()
    GUI.generate_timer.cancel()


def end_control():
    GUI.generate_timer.cancel()


schedule.every().day.at(Control_time_start_set).do(start_control)
schedule.every().day.at(Control_time_end_set).do(end_control)


def scheldue_job_pender():
    while True:
        schedule.run_pending()
        t.sleep(1)


ScldReportThread = Thread(target=scheldue_job_pender,)
ScldReportThread.start()


# generate_window_pos()

# root.withdraw()
# root.mainloop()
