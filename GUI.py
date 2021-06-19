import tkinter as tk
from threading import Timer, Thread, Event
from datetime import datetime, time, timedelta
import tkinter.font as font
from random import randint, choice
import cfg
from screeninfo import get_monitors
import logg
import users
import sys as sys
from pynput import keyboard

root = tk.Tk()
Config = cfg.config
### Конфиг окна проверки
# code_length = Config.read()['CheckWindowSettings']['CodeLength']
# use_symbols = Config.read()['CheckWindowSettings']['usedsymbols']
# btn_font = Config.read()['CheckWindowSettings']['btnfont']  # Размер шрифта
# code_font = Config.read()['CheckWindowSettings']['codefont']  # Размер шрифта
# okbuttonlabel = Config.read()['CheckWindowSettings']['okbuttonlabel']
# latebuttonlabel = Config.read()['CheckWindowSettings']['latebuttonlabel']
# win_size_multiplier = float(
#     Config.read()['CheckWindowSettings']['SizeMultiplier'])  # коэфициент размера окна относительно наименьшего монитора
### Конфиг Временных устаовок
# shift_start = Config.read()['TimeSettings']['shiftstart']
# shift_end = Config.read()['TimeSettings']['shiftend']
# report_send_time = Config.read()['TimeSettings']['ReportSendTime']
# min_window_appear_interval = Config.read()['TimeSettings']['MinWindowAppearInterval']
# max_window_appear_interval = Config.read()['TimeSettings']['MaxWindowAppearInterval']
# window_appear_duration = Config.read()['TimeSettings']['WindowAppearDuration']
# need_reaction_time = Config.read()['TimeSettings']['NeedReactionTime']
### Конфиг отчета
# emails = Config.read()['ReportSettings']['Emails']
# late_react_message = Config.read()['ReportSettings']['LateReactMsg']
# no_react_message = Config.read()['ReportSettings']['NoReactMsg']
# delimeter = Config.read()['ReportSettings']['Delimiter']


def generate_code(symbols,length):
    return ''.join(choice(symbols) for i in range(int(length)))


monitors = get_monitors()


# CheckWindow=tk.Toplevel(MainWindow)
# CheckWindow.overrideredirect(1)
# CheckWindow.wm_attributes("-topmost", True)

class CheckWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        # self.master.config(bg="black")
        self.master.overrideredirect(1)
        self.master.wm_attributes("-topmost", True)
        self.master.focus_force()

        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 1, weight=1)

        self.label_code = tk.Label(self.master, text=generate_code(Config.read()['CheckWindowSettings']['usedsymbols'],Config.read()['CheckWindowSettings']['codelength']))
        self.label_code.grid(row=0, columnspan=2)
        self.label_code['font'] = font.Font(size=Config.read()['CheckWindowSettings']['codefont'])

        self.btn_ack = tk.Button(self.master, text=Config.read()['CheckWindowSettings']['okbuttonlabel'])
        self.btn_ack.grid(row=1, column=0, sticky='we')
        self.btn_ack['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])

        self.btn_late = tk.Button(self.master, text=Config.read()['CheckWindowSettings']['latebuttonlabel'])
        self.btn_late.grid(row=1, column=1, sticky='we')
        self.btn_late['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])

        self.btn_ack.config(command=self.confirmation_success)
        self.btn_late.config(command=self.confirmation_late_success)

    window_appeared_at = datetime.now() ## иницализация переменной

    def confirmation_success(self):
        time_ack = datetime.now() - self.window_appeared_at
        window_appeared_at_time = self.window_appeared_at.strftime('%H:%M')
        minutes, seconds = divmod(int(time_ack.total_seconds()), 60)
        logg.logging.info('* %s * %s * %s * ОК * %s мин %s сек *', self.label_code.cget("text"),
                          window_appeared_at_time, datetime.now().strftime('%H:%M'),
                          minutes, seconds)
        self.master.withdraw()
        generate_timer._interval = generate_appear_interval()
        generate_timer.start()

    def confirmation_late_success(self):
        time_ack = datetime.now() - self.window_appeared_at
        window_appeared_at_time = self.window_appeared_at.strftime('%H:%M')
        logg.logging.info('Был на обходе ### (время появления окна:%s), ### (время реакции:%s)',
                          window_appeared_at_time,
                          time_ack)
        self.master.withdraw()
        generate_timer._interval = generate_appear_interval()
        generate_timer.start()


class SettingsWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.geometry('750x600')
        self.master.resizable(0, 0)
        self.master.title('Настройки')

        pady = 2
        padx = 5


        ### Список пользователей
        self.users_list = tk.LabelFrame(self.master, text='Список операторов')

        self.user_listbox = tk.Listbox(self.users_list)
        for i in users.get_all_users():
            self.user_listbox.insert(0, i)
        self.label_newuser=tk.Label(self.users_list, text="Логин")
        self.entry_newuser = tk.Entry(self.users_list)
        self.label_newpassword=tk.Label(self.users_list, text="Пароль")
        self.entry_newpassword = tk.Entry(self.users_list)

        tk.Grid.rowconfigure(self.users_list, 0, weight=10)
        tk.Grid.rowconfigure(self.users_list, 1, weight=1)
        tk.Grid.rowconfigure(self.users_list, 2, weight=1)

        self.user_listbox.grid(row=0, column=0,columnspan=2, padx=padx, pady=pady, sticky='nwe')

        self.label_newuser.grid(row=1, column=0,  sticky=tk.S)
        self.label_newpassword.grid(row=1, column=1,  sticky=tk.S)

        self.entry_newuser.grid(row=2, column=0, padx=padx, pady=pady, sticky=tk.N)
        self.entry_newpassword.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.N)
        # self.user_listbox.bind('<<ListboxSelect>>', self.onselect)
        self.addusrbtn = tk.Button(self.users_list, text='Добавить', width=7)
        self.addusrbtn.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.E)
        self.rmvusrbtn = tk.Button(self.users_list, text='Удалить', width=7)
        self.rmvusrbtn.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.rmvusrbtn.config(command=lambda: self.delete_user(self.user_listbox.get(self.user_listbox.curselection())[0]))
        self.addusrbtn.config(command= lambda:self.add_user(self.entry_newuser.get(),self.entry_newpassword.get()))

        # for self.i in Config['CheckWindowSettings']:
        #     self.i=tk.Label(CheckWindowsSettingsFrame, text="Начало интервала проверки (ЧЧ:ММ)")
        #     print(self.i)




        self.TimeSettingsFrame = tk.LabelFrame(self.master, text='Временные уставки')

        self.label_shiftstart = tk.Label(self.TimeSettingsFrame, text="Начало интервала проверки (ЧЧ:ММ)")
        self.entry_shiftstart = tk.Entry(self.TimeSettingsFrame, width=10)
        self.entry_shiftstart.insert(tk.END, Config.read()['TimeSettings']['shiftstart'])
        self.label_shiftend = tk.Label(self.TimeSettingsFrame, text="Конец интервала проверки (ЧЧ:ММ)")
        self.entry_shiftend = tk.Entry(self.TimeSettingsFrame, width=10)
        self.entry_shiftend.insert(tk.END, Config.read()['TimeSettings']['shiftend'])

        self.label_reporttime = tk.Label(self.TimeSettingsFrame, text='Время отправки ежедн. отчета(ЧЧ:ММ)')
        self.entry_reporttime = tk.Entry(self.TimeSettingsFrame, width=10)
        self.entry_reporttime.insert(tk.END, Config.read()['TimeSettings']['ReportSendTime'])

        self.label_mincodetime = tk.Label(self.TimeSettingsFrame, text='Минимальное время появления кода (мин)')
        self.entry_mincodetime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_mincodetime.insert(tk.END, Config.read()['TimeSettings']['MinWindowAppearInterval'])

        self.label_maxcodetime = tk.Label(self.TimeSettingsFrame, text='Максимальное время появления кода (мин)')
        self.entry_maxcodetime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_maxcodetime.insert(tk.END, Config.read()['TimeSettings']['MaxWindowAppearInterval'])

        self.label_codedurationtime = tk.Label(self.TimeSettingsFrame, text='Длительность отображения окна (сек)')
        self.entry_codedurationtime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_codedurationtime.insert(tk.END, Config.read()['TimeSettings']['WindowAppearDuration'])

        self.label_reacttime = tk.Label(self.TimeSettingsFrame, text='Необходимое время реакции (сек)')
        self.entry_reacttime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_reacttime.insert(tk.END, Config.read()['TimeSettings']['NeedReactionTime'])

        self.label_shiftstart.grid(row=0, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_shiftstart.grid(row=0, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_shiftend.grid(row=1, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_shiftend.grid(row=1, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_reporttime.grid(row=2, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_reporttime.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_mincodetime.grid(row=3, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_mincodetime.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_maxcodetime.grid(row=4, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_maxcodetime.grid(row=4, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_codedurationtime.grid(row=5, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_codedurationtime.grid(row=5, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.label_reacttime.grid(row=6, column=0, padx=padx, pady=pady, sticky=tk.E)
        self.entry_reacttime.grid(row=6, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.CheckWindowsSettingsFrame = tk.LabelFrame(self.master, text='Проверочное окно')

        tk.Grid.columnconfigure(self.CheckWindowsSettingsFrame, 0, weight=2)
        tk.Grid.columnconfigure(self.CheckWindowsSettingsFrame, 1, weight=1)

        self.label_usesymbols = tk.Label(self.CheckWindowsSettingsFrame, text='Символы контрольного сообщения')
        self.entry_usesymbols = tk.Entry(self.CheckWindowsSettingsFrame)
        self.entry_usesymbols.insert(tk.END, Config.read()['CheckWindowSettings']['usedsymbols'])

        self.label_numsymbols = tk.Label(self.CheckWindowsSettingsFrame, text='Количество символов')
        self.entry_numsymbols = tk.Entry(self.CheckWindowsSettingsFrame, width=5)
        self.entry_numsymbols.insert(tk.END, Config.read()['CheckWindowSettings']['CodeLength'])

        self.label_codefont = tk.Label(self.CheckWindowsSettingsFrame, text='Размер шрифта кода')
        self.entry_codefont = tk.Entry(self.CheckWindowsSettingsFrame, width=5)
        self.entry_codefont.insert(tk.END, Config.read()['CheckWindowSettings']['codefont'])

        self.label_okbuttonlabel = tk.Label(self.CheckWindowsSettingsFrame, text='Надпись на кнопке 1')
        self.entry_okbuttonlabel = tk.Entry(self.CheckWindowsSettingsFrame)
        self.entry_okbuttonlabel.insert(tk.END, Config.read()['CheckWindowSettings']['okbuttonlabel'])

        self.label_latebuttonlabel = tk.Label(self.CheckWindowsSettingsFrame, text='Надпись на кнопке 2')
        self.entry_latebuttonlabel = tk.Entry(self.CheckWindowsSettingsFrame)
        self.entry_latebuttonlabel.insert(tk.END, Config.read()['CheckWindowSettings']['latebuttonlabel'])

        self.label_buttonfont = tk.Label(self.CheckWindowsSettingsFrame, text='Размер шрифта на кнопках')
        self.entry_buttonfont = tk.Entry(self.CheckWindowsSettingsFrame, width=5)
        self.entry_buttonfont.insert(tk.END, Config.read()['CheckWindowSettings']['btnfont'])

        self.label_sizemultiplier = tk.Label(self.CheckWindowsSettingsFrame, text='Коэффициент размера окна')
        self.entry_sizemultiplier = tk.Entry(self.CheckWindowsSettingsFrame, width=5)
        self.entry_sizemultiplier.insert(tk.END, float(Config.read()['CheckWindowSettings']['SizeMultiplier']))



        self.button_showcheckwindow = tk.Button(self.CheckWindowsSettingsFrame, text='Показать окно')
        self.button_showcheckwindow.grid(row=11, column=1, sticky=tk.W)
        self.button_showcheckwindow.config(command=self.show_checkwindow)

        # self.button_hidecheckwindow = tk.Button(self.CheckWindowsSettingsFrame, text='Скрыть окно')
        # self.button_hidecheckwindow.grid(row=11, column=0, sticky=tk.E)
        # self.button_hidecheckwindow.config(command=self.hide_checkwindow)

        self.label_usesymbols.grid(row=4, column=0, sticky=tk.E)
        self.entry_usesymbols.grid(row=4, column=1)

        self.label_numsymbols.grid(row=5, column=0, sticky=tk.E)
        self.entry_numsymbols.grid(row=5, column=1, sticky=tk.W)

        self.label_codefont.grid(row=6, column=0, sticky=tk.E)
        self.entry_codefont.grid(row=6, column=1, sticky=tk.W)

        self.label_okbuttonlabel.grid(row=7, column=0, sticky=tk.E)
        self.entry_okbuttonlabel.grid(row=7, column=1)

        self.label_latebuttonlabel.grid(row=8, column=0, sticky=tk.E)
        self.entry_latebuttonlabel.grid(row=8, column=1)

        self.label_buttonfont.grid(row=9, column=0, sticky=tk.E)
        self.entry_buttonfont.grid(row=9, column=1, sticky=tk.W)

        self.label_sizemultiplier.grid(row=10, column=0, sticky=tk.E)
        self.entry_sizemultiplier.grid(row=10, column=1, sticky=tk.W)

        self.ReportSettingsFrame = tk.LabelFrame(self.master, text='Настройки отчета')



        self.label_email = tk.Label(self.ReportSettingsFrame, text='Эл. почта для рассылки(через ";")')
        self.entry_email = tk.Entry(self.ReportSettingsFrame)
        self.entry_email.insert(tk.END, Config.read()['ReportSettings']['Emails'])

        self.label_reacttimetxt = tk.Label(self.ReportSettingsFrame, text='Сообщение [время реакции превышено]')
        self.entry_reacttimetxt = tk.Entry(self.ReportSettingsFrame)
        self.entry_reacttimetxt.insert(tk.END, Config.read()['ReportSettings']['LateReactMsg'])

        self.label_noreacttxt = tk.Label(self.ReportSettingsFrame, text='Сообщение [реакции небыло]')
        self.entry_noreacttxt = tk.Entry(self.ReportSettingsFrame)
        self.entry_noreacttxt.insert(tk.END, Config.read()['ReportSettings']['NoReactMsg'])

        self.label_delimeter = tk.Label(self.ReportSettingsFrame, text='Разделитель')
        self.entry_delimeter = tk.Entry(self.ReportSettingsFrame, width=5)
        self.entry_delimeter.insert(tk.END, Config.read()['ReportSettings']['Delimiter'])

        self.label_email.grid(row=3, column=0, sticky=tk.E)
        self.entry_email.grid(row=3, column=1)

        self.label_reacttimetxt.grid(row=14, column=0, sticky=tk.E)
        self.entry_reacttimetxt.grid(row=14, column=1)

        self.label_noreacttxt.grid(row=15, column=0, sticky=tk.E)
        self.entry_noreacttxt.grid(row=15, column=1)

        self.label_delimeter.grid(row=16, column=0, sticky=tk.E)
        self.entry_delimeter.grid(row=16, column=1, sticky=tk.W)

        self.AdminSettingsFrame = tk.LabelFrame(self.master, text='Прочие настройки')

        self.label_adminpassword = tk.Label(self.ReportSettingsFrame, text='Пароль администратора')
        self.entry_adminpassword = tk.Entry(self.ReportSettingsFrame)
        self.entry_adminpassword.insert(tk.END, cfg.config.read()['AdminSettings']['Password'])

        self.label_adminpassword.grid(row=0, column=0, sticky=tk.E)
        self.entry_adminpassword.grid(row=0, column=1, sticky=tk.W)

        self.applybtn = tk.Button(self.master, text='Применить')
        self.applybtn.pack(side=tk.BOTTOM)
        self.applybtn.config(command=self.update_config)



        self.changeusrbtn = tk.Button(self.master, text='Сменить пользователя')
        self.changeusrbtn.pack(side=tk.BOTTOM)
        self.changeusrbtn.config(command=self.change_user)

        self.quitbtn = tk.Button(self.master, text='Выход')
        self.quitbtn.pack(side=tk.BOTTOM)
        self.quitbtn.config(command=self.quit)

        self.users_list.pack(padx=10, pady=5, side=tk.RIGHT, fill=tk.BOTH)
        self.TimeSettingsFrame.pack(padx=10, pady=5, anchor=tk.NW)
        self.CheckWindowsSettingsFrame.pack(padx=10, pady=5, anchor=tk.NW)
        self.ReportSettingsFrame.pack(padx=10, pady=5, anchor=tk.NW)
        self.AdminSettingsFrame.pack(padx=10, pady=5, anchor=tk.NW)
    def refresh_user_list(self,):
        self.user_listbox.delete(0, tk.END)
        for i in users.get_all_users():
            self.user_listbox.insert(0, i)

    def add_user(self,user,password):
        if not users.is_in_csv(user) and user != 'username':
            users.add_account(user, password)
            self.refresh_user_list()
        else: return None

    def delete_user(self,user):
        users.delete_account(user)
        self.refresh_user_list()

    # def onselect(self,event):
    #         w = event.widget
    #         idx = int(w.curselection()[0])
    #         value = w.get(idx)
    #         print(value)

    def change_user(self,):
        self.master.withdraw()
        login_window.show()

    def quit(self,):
        timer_missed.cancel()
        generate_timer.cancel()
        self.master.after(1000, root.destroy())
        sys.exit(0)


    def show_checkwindow(self,):
            if not test_check_window.master.winfo_viewable():
                test_check_window.master.deiconify()
            test_check_window.label_code['font'] = font.Font(size=self.entry_codefont.get())
            test_check_window.label_code['text'] = generate_code(self.entry_usesymbols.get(),self.entry_numsymbols.get())
            test_check_window.btn_ack['font'] = font.Font(size=self.entry_buttonfont.get())
            test_check_window.btn_ack['text'] = self.entry_okbuttonlabel.get()
            test_check_window.btn_late['font'] = font.Font(size=self.entry_buttonfont.get())
            test_check_window.btn_late['text'] = self.entry_latebuttonlabel.get()
            auto_window_size(test_check_window,self.entry_sizemultiplier.get())

    def hide_checkwindow(self,):
        test_check_window.master.withdraw()

    def update_config(self,):
        Config.settings.set('TimeSettings','shiftstart',self.entry_shiftstart.get())
        Config.settings.set('TimeSettings', 'shiftend', self.entry_shiftend.get())
        Config.settings.set('TimeSettings', 'ReportSendTime', self.entry_reporttime.get())
        Config.settings.set('TimeSettings', 'MinWindowAppearInterval', self.entry_mincodetime.get())
        Config.settings.set('TimeSettings', 'MaxWindowAppearInterval', self.entry_maxcodetime.get())
        Config.settings.set('TimeSettings', 'WindowAppearDuration', self.entry_codedurationtime.get())
        Config.settings.set('TimeSettings', 'NeedReactionTime', self.entry_reacttime.get())
        Config.write()
        self.refresh_config()

    def refresh_config(self,):
        self.entry_shiftstart.delete(0, tk.END)
        self.entry_shiftend.delete(0, tk.END)
        self.entry_reporttime.delete(0, tk.END)
        self.entry_mincodetime.delete(0, tk.END)
        self.entry_maxcodetime.delete(0, tk.END)
        self.entry_codedurationtime.delete(0, tk.END)
        self.entry_reacttime.delete(0, tk.END)

        self.entry_shiftstart.insert(tk.END, Config.read()['TimeSettings']['shiftstart'])
        self.entry_shiftend.insert(tk.END, Config.read()['TimeSettings']['shiftend'])
        self.entry_reporttime.insert(tk.END, Config.read()['TimeSettings']['ReportSendTime'])
        self.entry_mincodetime.insert(tk.END, Config.read()['TimeSettings']['MinWindowAppearInterval'])
        self.entry_maxcodetime.insert(tk.END, Config.read()['TimeSettings']['MaxWindowAppearInterval'])
        self.entry_codedurationtime.insert(tk.END, Config.read()['TimeSettings']['WindowAppearDuration'])
        self.entry_reacttime.insert(tk.END, Config.read()['TimeSettings']['NeedReactionTime'])

        self.entry_delimeter.insert(tk.END, Config.read()['ReportSettings']['Delimiter'])

def disable_event():
            pass

class LoginWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title('Вход в систему')
        w = 250
        h = 100

        self.master.resizable(0, 0)
        # self.master.overrideredirect(1)
        # configure the grid
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.master.protocol("WM_DELETE_WINDOW", disable_event)

        tk.Grid.columnconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 1, weight=2)

        # username
        username_label = tk.Label(self.master, text="Логин:")
        username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        username_entry = tk.Entry(self.master)
        username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # password
        password_label = tk.Label(self.master, text="Пароль:")
        password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        password_entry = tk.Entry(self.master, show="*")
        password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # login button
        login_button = tk.Button(self.master, text="Войти")
        login_button.grid(column=1, row=3, sticky=tk.N, padx=5, pady=5)

        def login():
            if username_entry.get() == 'admin' and password_entry.get() == cfg.config.read()['AdminSettings']['Password']:
                password_entry.delete(0, tk.END)
                username_entry.delete(0, tk.END)
                settings_window.master.deiconify()
                settings_window.master.focus_set()
                self.master.withdraw()

        login_button.config(command=login)

    def show(self):
        self.master.deiconify()
        self.master.focus()


# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer = None
#         self.interval = interval
#         self.function = function
#         self.args = args
#         self.kwargs = kwargs
#         self.is_running = False
#
#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)
#
#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True
#
#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False

def generate_appear_interval():
    intrvl = randint(int(Config.read()['TimeSettings']['MinWindowAppearInterval']) * 60,
                     int(Config.read()['TimeSettings']['MaxWindowAppearInterval']) * 60)
    print(intrvl)
    print((datetime.now() + timedelta(seconds=intrvl)))
    return intrvl


def generate_window_pos():
    auto_window_size(check_window,Config.read()['CheckWindowSettings']['SizeMultiplier'])
    rand_display_num = randint(1, len(monitors)) - 1
    bottom_border = monitors[rand_display_num].height - window_height
    right_border = monitors[rand_display_num].width - window_width
    [monitor_x, monitor_y] = [monitors[rand_display_num].x, monitors[rand_display_num].y]
    windset_pos_x = randint(monitor_x, monitor_x + right_border)
    windset_pos_y = randint(monitor_y, monitor_y + bottom_border)
    check_window.master.geometry('+%d+%d' % (windset_pos_x, windset_pos_y))
    # print('Window_x:', windset_pos_x, 'Window_y:', windset_pos_y, 'Monitor_x:', monitor_x, 'Monitor_y:', monitor_y)
    if not timer_missed._interval == 0:
        timer_missed.start()
    check_window.window_appeared_at = datetime.now()
    check_window.label_code['text'] = generate_code(Config.read()['CheckWindowSettings']['usedsymbols'],Config.read()['CheckWindowSettings']['codelength'])
    check_window.master.deiconify()


def confirmation_missed():
    if check_window.master.winfo_viewable():
        time_miss = datetime.now() - check_window.window_appeared_at
        window_appeared_at_time = check_window.window_appeared_at.strftime('%H:%M')
        logg.logging.info('Не квитировано !!! (время появления:%s),(прошло времени:%s)', window_appeared_at_time,
                          time_miss)
        check_window.master.withdraw()
        # gc.collect()
        # print(gc.get_objects())
        # tracker.print_diff()
        generate_timer._interval = generate_appear_interval()
        generate_timer.start()


# timer_missed=Timer(3.0, confirmation_missed)
class RepeatableTimer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.t = Timer(self._interval, self._function, *self._args, **self._kwargs)
    def start(self):
        self.t.start()

    def cancel(self):
        self.t.cancel()


timer_missed = RepeatableTimer(int(Config.read()['TimeSettings']['WindowAppearDuration']), confirmation_missed,() )
generate_timer = RepeatableTimer(None, generate_window_pos, ())


def auto_window_size(window,multiplier):
    global window_height
    global window_width
    min_display_height = min(m.height for m in monitors)
    min_display_width = min(m.width for m in monitors)
    window_height = int(min_display_height * float(multiplier))
    window_width = int(min_display_width * float(multiplier))
    window.master.geometry('%dx%d' % (window_width, window_height))


################### ОЧЕНЬ ПЛОХО!!!!!!!!!!!!!!!!!!!!??#####################################
def listener_thread():
    def on_activate():
        if not settings_window.master.winfo_viewable():
            login_window.show()
            # login_window.master.focus()
            login_window.master.attributes('-topmost',True)
            print('Global hotkey activated!')

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+]'),
        on_activate)

    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()

# class StoppableThread(Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""
#
#     def __init__(self,  *args, **kwargs):
#         super(StoppableThread, self).__init__(*args, **kwargs)
#         self._stop_event = Event()
#
#     def stop(self):
#         self._stop_event.set()
#
#     def stopped(self):
#         return self._stop_event.is_set()
#
# key_listener_thread = StoppableThread(target=listener_thread, )
key_listener_thread = Thread(target=listener_thread, )
key_listener_thread.daemon = True
key_listener_thread.start()

#########################################################################

settings_window = SettingsWindow(root)
login_window = LoginWindow(root)
check_window = CheckWindow(root)

######
test_check_window = CheckWindow(root)
test_check_window.master.title('Пример проверочного окна')
test_check_window.master.withdraw()
test_check_window.master.resizable(0,0)
test_check_window.master.attributes('-toolwindow', True)
test_check_window.master.geometry('+%d+%d' % (int(root.winfo_screenwidth()/2),
                                  int(root.winfo_screenheight()/2)))
test_check_window.  btn_ack.config(command=disable_event)
test_check_window.btn_late.config(command=disable_event)
test_check_window.master.protocol("WM_DELETE_WINDOW", settings_window.hide_checkwindow)
test_check_window.master.overrideredirect(0)
test_check_window.master.wm_attributes("-topmost", True)


# def show_checkwindow():
#     if not test_check_window.master.winfo_viewable():
#         test_check_window.master.deiconify()
#     test_check_window.master.overrideredirect(0)
#     test_check_window.master.wm_attributes("-topmost", True)
#
#     test_check_window.label_code['font'] = font.Font(size=Config.read()['CheckWindowSettings']['codefont'])
#     test_check_window.label_code['text'] = generate_code()
#     test_check_window.btn_ack['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])
#     test_check_window.btn_ack['text'] = Config.read()['CheckWindowSettings']['okbuttonlabel']
#     test_check_window.btn_late['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])
#     test_check_window.btn_late['text'] = Config.read()['CheckWindowSettings']['latebuttonlabel']


# SettingsWindow.master.withdraw()
check_window.master.withdraw()
# auto_window_size(check_window)

generate_window_pos()

root.withdraw()
root.mainloop()

# with keyboard.Listener(
#         on_press=for_canonical(hotkey.press),
#         on_release=for_canonical(hotkey.release)) as l:
#     l.join()
# Config.write()