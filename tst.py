from pynput import keyboard

# def on_press(key):
#     if key == keyboard.Key.f7
#
# keyboard.Listener(on_press=on_press).run()aa

# COMBINATION = { keyboard.Key.ctrl,'q' }
#
# # The currently active modifiers
# current = set()
#
#
# def on_press(key):
#     if key in COMBINATION:
#         current.add(key)
#         if all(k in current for k in COMBINATION):
#             print('All modifiers active!')
#     if key == keyboard.Key.esc:
#         listener.stop()
#
#
# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass
#
#
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()


# def on_activate():
#     print('Global hotkey activated!')
#
# def for_canonical(f):
#     return lambda k: f(l.canonical(k))
#
# hotkey = keyboard.HotKey(
#     keyboard.HotKey.parse('<ctrl>+]'),
#     on_activate)
# with keyboard.Listener(
#         on_press=for_canonical(hotkey.press),
#         on_release=for_canonical(hotkey.release)) as l:
#     l.join()

# listener = keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release),suppress=True)
# listener.start()


# account = []
# account.append('user')
# account.append('password')
# print((account))

# import os
# import logg
# import time
# import datetime as dt
#
#
# def filetest():
#     outf = logg.month_log_folder + "/" + (dt.datetime.fromtimestamp(time.time())-dt.timedelta(days=1)).strftime('%Y_%m') + ".log"
#     with open(outf, "wb") as outfile:
#         for f in os.listdir(logg.month_log_folder):
#             filename = logg.month_log_folder + "/" + f
#             with open(filename, "rb") as infile:
#                 outfile.write(infile.read())
#
#
# filetest()

import cfg
import report
import logg
import datetime as dt

report.send_mail(
                send_from='IndifferentD@yandex.ru',
                 # send_to=cfg.config.read()['AdminSettings']['Emails'],
                send_to=['IndifferentD@yandex.ru'],
                 subject='Контроль оператора',
                 message='',
                 files=[logg.LOG_FILE],
                 # files=[],
                 # server=cfg.config.read()['AdminSettings']['SmtpServer'],
                    server='smtp.yandex.ru',
                 # port=cfg.config.read()['AdminSettings']['EmailPort'],
                 port='587',
                 # username=cfg.config.read()['AdminSettings']['Email'],
                 username='IndifferentD@yandex.ru',
                 # password=cfg.config.read()['AdminSettings']['EmailPassword'],
                 password='1qazZAQ!qwe',
                 use_tls=True)
