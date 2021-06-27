import tkinter as tk
from threading import Timer, Thread
from datetime import datetime, timedelta
import tkinter.font as font
from time import strptime, localtime
from random import randint, choice
import cfg
from screeninfo import get_monitors
import logg
import users
import sys as sys
from pynput import keyboard
import report
from Main import init_jobs, start_control


def generate_code(symbols, length):
    return ''.join(choice(symbols) for _ in range(int(length)))


# Exception catcher
import traceback
import tkinter.messagebox


# You would normally put that on the App class
def show_error(self, *args):
    err = traceback.format_exception(*args)
    tkinter.messagebox.showerror('Exception', err)


# but this works too
tk.Tk.report_callback_exception = show_error


# #


class CheckWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.overrideredirect(1)
        self.master.wm_attributes("-topmost", True)
        self.master.focus_force()

        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 1, weight=1)

        self.label_code = tk.Label(self.master, text=generate_code(Config.read()['CheckWindowSettings']['usedsymbols'],
                                                                   Config.read()['CheckWindowSettings']['codelength']))
        self.label_code.grid(row=0, columnspan=2)
        self.label_code['font'] = font.Font(size=Config.read()['CheckWindowSettings']['codefont'])

        self.btn_ack = tk.Button(self.master, text=Config.read()['CheckWindowSettings']['okbuttonlabel'])
        self.btn_ack.grid(row=1, column=0, sticky='we')
        self.btn_ack['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])

        self.btn_late = tk.Button(self.master, text=Config.read()['CheckWindowSettings']['latebuttonlabel'])
        self.btn_late.grid(row=1, column=1, sticky='we')
        self.btn_late['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])

        self.btn_ack.config(command=lambda state="ok": self.confirmation(state))
        self.btn_late.config(command=lambda state="late": self.confirmation(state))

    def update_settings(self, ):
        self.label_code['font'] = font.Font(size=Config.read()['CheckWindowSettings']['codefont'])
        self.btn_ack['text'] = Config.read()['CheckWindowSettings']['okbuttonlabel']
        self.btn_late['text'] = Config.read()['CheckWindowSettings']['latebuttonlabel']
        self.btn_ack['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])
        self.btn_late['font'] = font.Font(size=Config.read()['CheckWindowSettings']['btnfont'])

    window_appeared_at = datetime.now()  # иницализация переменной

    def confirmation(self, state):
        time_to_ack = datetime.now() - self.window_appeared_at
        window_appeared_at_time = self.window_appeared_at.strftime('%H:%M')
        minutes, seconds = divmod(int(time_to_ack.total_seconds()), 60)
        if state == 'ok':
            btntext = self.btn_ack['text']
        else:
            btntext = self.btn_late['text']
        logg.logging.info('* %s * %s * %s * %s * %s * %s мин %s сек *', current_user,
                          self.label_code.cget("text"),
                          window_appeared_at_time, datetime.now().strftime('%H:%M'),
                          btntext,
                          minutes, seconds)
        self.master.withdraw()
        start_reveal_timer()


class SettingsWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.geometry('750x560')
        self.master.resizable(0, 0)
        self.master.title('Настройки')

        pady = 2
        padx = 5

        self.topframe = tk.Frame(self.master)
        self.botframe = tk.Frame(self.master)
        self.buttonsframe = tk.Frame(self.master)
        self.topframe.pack()
        self.botframe.pack()
        self.buttonsframe.pack()

        self.CheckWindowsSettingsFrame = tk.LabelFrame(self.topframe, text='Проверочное окно')
        self.users_list = tk.LabelFrame(self.topframe, text='Список операторов')
        self.TimeSettingsFrame = tk.LabelFrame(self.botframe, text='Временные уставки')
        self.TimeSettingsFrame.pack_propagate(0)
        self.AdminSettingsFrame = tk.LabelFrame(self.botframe, text='Прочие настройки')

        self.CheckWindowsSettingsFrame.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.BOTH)
        self.users_list.pack(padx=10, pady=5, side=tk.RIGHT, fill=tk.BOTH)

        self.AdminSettingsFrame.pack(padx=10, pady=5, side=tk.RIGHT, fill=tk.Y)
        self.TimeSettingsFrame.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.BOTH)

        self.applybtn = tk.Button(self.buttonsframe, text='Применить')
        self.applybtn.pack(side=tk.LEFT, padx=3)
        self.applybtn.config(command=self.apply_settings)

        self.quitbtn = tk.Button(self.buttonsframe, text='Выход')
        self.quitbtn.pack(side=tk.RIGHT, padx=(400, 0))
        self.quitbtn.config(command=self.quit)

        self.changeusrbtn = tk.Button(self.buttonsframe, text='Сменить пользователя')
        self.changeusrbtn.pack(side=tk.LEFT, padx=3)
        self.changeusrbtn.config(command=self.change_user)

        # Список пользователей

        self.user_listbox = tk.Listbox(self.users_list)
        for i in users.get_all_users():
            self.user_listbox.insert(0, i)
        self.label_newuser = tk.Label(self.users_list, text="Логин")
        self.entry_newuser = tk.Entry(self.users_list)
        self.label_newpassword = tk.Label(self.users_list, text="Пароль")
        self.entry_newpassword = tk.Entry(self.users_list)

        tk.Grid.rowconfigure(self.users_list, 0, weight=10)
        tk.Grid.rowconfigure(self.users_list, 1, weight=1)
        tk.Grid.rowconfigure(self.users_list, 2, weight=1)

        self.user_listbox.grid(row=0, column=0, columnspan=2, padx=padx, pady=pady, sticky='nwe')

        self.label_newuser.grid(row=1, column=0, sticky=tk.S)
        self.label_newpassword.grid(row=1, column=1, sticky=tk.S)

        self.entry_newuser.grid(row=2, column=0, padx=padx, pady=pady, sticky=tk.N)
        self.entry_newpassword.grid(row=2, column=1, padx=padx, pady=pady, sticky=tk.N)
        # self.user_listbox.bind('<<ListboxSelect>>', self.onselect)
        self.addusrbtn = tk.Button(self.users_list, text='Добавить', width=7)
        self.addusrbtn.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.E)
        self.rmvusrbtn = tk.Button(self.users_list, text='Удалить', width=7)
        self.rmvusrbtn.grid(row=3, column=1, padx=padx, pady=pady, sticky=tk.W)

        self.rmvusrbtn.config(command=self.delete_user)
        self.addusrbtn.config(command=lambda: self.add_user(self.entry_newuser.get(), self.entry_newpassword.get()))

        # for self.i in Config['CheckWindowSettings']:
        #     self.i=tk.Label(CheckWindowsSettingsFrame, text="Начало интервала проверки (ЧЧ:ММ)")
        #     print(self.i)

        self.label_shiftstart = tk.Label(self.TimeSettingsFrame, text="Начало интервала проверки (ЧЧ:ММ)")
        self.entry_shiftstart = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_shiftstart.insert(tk.END, Config.read()['TimeSettings']['shiftstart'])

        self.label_shiftend = tk.Label(self.TimeSettingsFrame, text="Конец интервала проверки (ЧЧ:ММ)")
        self.entry_shiftend = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_shiftend.insert(tk.END, Config.read()['TimeSettings']['shiftend'])

        self.label_reporttime = tk.Label(self.TimeSettingsFrame, text='Время отправки ежедн. отчета(ЧЧ:ММ)')
        self.entry_reporttime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_reporttime.insert(tk.END, Config.read()['TimeSettings']['ReportSendTime'])

        self.label_mincodetime = tk.Label(self.TimeSettingsFrame, text='Минимальный интервал появления кода (мин)')
        self.entry_mincodetime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_mincodetime.insert(tk.END, Config.read()['TimeSettings']['MinWindowAppearInterval'])

        self.label_maxcodetime = tk.Label(self.TimeSettingsFrame, text='Максимальный интервал появления кода (мин)')
        self.entry_maxcodetime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_maxcodetime.insert(tk.END, Config.read()['TimeSettings']['MaxWindowAppearInterval'])

        self.label_codedurationtime = tk.Label(self.TimeSettingsFrame, text='Длительность отображения окна (сек)')
        self.entry_codedurationtime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_codedurationtime.insert(tk.END, Config.read()['TimeSettings']['WindowAppearDuration'])

        self.label_reacttime = tk.Label(self.TimeSettingsFrame, text='Необходимое время реакции (сек)')
        self.entry_reacttime = tk.Entry(self.TimeSettingsFrame, width=5)
        self.entry_reacttime.insert(tk.END, Config.read()['TimeSettings']['NeedReactionTime'])

        self.time_settings_labels = [self.label_shiftstart, self.label_shiftend, self.label_reporttime,
                                     self.label_mincodetime, self.label_maxcodetime, self.label_codedurationtime,
                                     self.label_reacttime]
        self.time_settings_entries = [self.entry_shiftstart, self.entry_shiftend, self.entry_reporttime,
                                      self.entry_mincodetime, self.entry_maxcodetime, self.entry_codedurationtime,
                                      self.entry_reacttime]

        for idx, (l, e) in enumerate(zip(self.time_settings_labels, self.time_settings_entries)):
            l.grid(row=idx, column=0, sticky=tk.E)
            if idx == 0:
                e.grid(row=idx, column=1, sticky=tk.W, padx=(0, 5))
            else:
                e.grid(row=idx, column=1, sticky=tk.W)

        tk.Grid.columnconfigure(self.CheckWindowsSettingsFrame, 0, weight=2)
        tk.Grid.columnconfigure(self.CheckWindowsSettingsFrame, 1, weight=1)

        self.label_usesymbols = tk.Label(self.CheckWindowsSettingsFrame, text='Символы контрольного сообщения')
        self.entry_usesymbols = tk.Text(self.CheckWindowsSettingsFrame, width=25, height=6)
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

        self.button_showcheckwindow = tk.Button(self.CheckWindowsSettingsFrame, text='Сгенерировать окно')
        self.button_showcheckwindow.grid(row=11, column=1, sticky=tk.W)
        self.button_showcheckwindow.config(command=self.show_checkwindow)

        self.randwinpos = tk.IntVar()
        self.check_randwindpos = tk.Checkbutton(self.CheckWindowsSettingsFrame, text='Случайная позиция',
                                                variable=self.randwinpos)
        self.check_randwindpos.grid(row=11, column=0, sticky=tk.E)

        self.check_windows_settings_labels = [self.label_usesymbols, self.label_numsymbols, self.label_codefont,
                                              self.label_buttonfont, self.label_okbuttonlabel,
                                              self.label_latebuttonlabel, self.label_sizemultiplier]
        self.check_windows_settings_entries = [self.entry_usesymbols, self.entry_numsymbols, self.entry_codefont,
                                               self.entry_buttonfont, self.entry_okbuttonlabel,
                                               self.entry_latebuttonlabel, self.entry_sizemultiplier]

        # Проход по спискам ентриев и лейблов в фрейме настроек проверочного окна: расстановка по сетке
        for idx, (l, e) in enumerate(zip(self.check_windows_settings_labels, self.check_windows_settings_entries)):
            l.grid(row=idx, column=0, sticky=tk.E)
            if idx == 0:
                e.grid(row=idx, column=1, sticky=tk.W, padx=(0, 5))
            else:
                e.grid(row=idx, column=1, sticky=tk.W)

        self.label_adminpassword = tk.Label(self.AdminSettingsFrame, text='Пароль администратора')
        self.entry_adminpassword = tk.Entry(self.AdminSettingsFrame)
        self.entry_adminpassword.insert(tk.END, cfg.config.read()['AdminSettings']['Password'])

        self.label_email = tk.Label(self.AdminSettingsFrame, text='Эл. почта для рассылки(через ";")')
        self.entry_email = tk.Entry(self.AdminSettingsFrame)
        self.entry_email.insert(tk.END, Config.read()['AdminSettings']['Emails'])

        self.label_reacttimetxt = tk.Label(self.AdminSettingsFrame, text='Сообщение [время превышено]')
        self.entry_reacttimetxt = tk.Entry(self.AdminSettingsFrame)
        self.entry_reacttimetxt.insert(tk.END, Config.read()['AdminSettings']['LateReactMsg'])

        self.label_noreacttxt = tk.Label(self.AdminSettingsFrame, text='Сообщение [реакции не было]')
        self.entry_noreacttxt = tk.Entry(self.AdminSettingsFrame)
        self.entry_noreacttxt.insert(tk.END, Config.read()['AdminSettings']['NoReactMsg'])

        self.label_delimeter = tk.Label(self.AdminSettingsFrame, text='Разделитель')
        self.entry_delimeter = tk.Entry(self.AdminSettingsFrame, width=5)
        self.entry_delimeter.insert(tk.END, Config.read()['AdminSettings']['Delimiter'])

        self.label_emailuse = tk.Label(self.AdminSettingsFrame, text='Логин эл. почты')
        self.entry_emailuse = tk.Entry(self.AdminSettingsFrame)
        self.entry_emailuse.insert(tk.END, Config.read()['AdminSettings']['Email'])

        self.label_emailusepswd = tk.Label(self.AdminSettingsFrame, text='Пароль эл. почты')
        self.entry_emailusepswd = tk.Entry(self.AdminSettingsFrame)
        self.entry_emailusepswd.insert(tk.END, Config.read()['AdminSettings']['EmailPassword'])

        self.label_emailuseport = tk.Label(self.AdminSettingsFrame, text='Порт')
        self.entry_emailuseport = tk.Entry(self.AdminSettingsFrame, width=5)
        self.entry_emailuseport.insert(tk.END, Config.read()['AdminSettings']['EmailPort'])

        self.label_smtpserver = tk.Label(self.AdminSettingsFrame, text='smtp-сервер')
        self.entry_smtpserver = tk.Entry(self.AdminSettingsFrame)
        self.entry_smtpserver.insert(tk.END, Config.read()['AdminSettings']['SmtpServer'])

        self.tstemailbtn = tk.Button(self.AdminSettingsFrame, text='Тестовое письмо', width=15)
        self.tstemailbtn.config(command=lambda: report.send_mail(send_from=self.entry_emailuse.get(),
                                                                 send_to=self.entry_emailuse.get(),
                                                                 port=self.entry_emailuseport.get(),
                                                                 username=self.entry_emailuse.get(),
                                                                 password=self.entry_emailusepswd.get(),
                                                                 subject='Тестовое письмо',
                                                                 server=self.entry_smtpserver.get(),
                                                                 message='Отправлено %s' % datetime.now()))

        self.admin_settings_labels = [self.label_adminpassword, self.label_email, self.label_reacttimetxt,
                                      self.label_noreacttxt, self.label_delimeter, self.label_emailuse,
                                      self.label_emailusepswd, self.label_emailuseport, self.label_smtpserver]
        self.admin_settings_entries = [self.entry_adminpassword, self.entry_email, self.entry_reacttimetxt,
                                       self.entry_noreacttxt, self.entry_delimeter, self.entry_emailuse,
                                       self.entry_emailusepswd, self.entry_emailuseport, self.entry_smtpserver]

        for idx, (l, e) in enumerate(zip(self.admin_settings_labels, self.admin_settings_entries)):
            l.grid(row=idx, column=0, sticky=tk.E)
            e.grid(row=idx, column=1, sticky=tk.W)

        self.tstemailbtn.grid(row=9, column=1, padx=padx, pady=pady, sticky=tk.W)

    def refresh_user_list(self, ):
        self.user_listbox.delete(0, tk.END)
        for i in users.get_all_users():
            self.user_listbox.insert(0, i)

    def add_user(self, user, password):
        if not users.is_in_userlist(user) and user != '':
            users.add_account(user, password)
            self.refresh_user_list()
        else:
            return None

    def delete_user(self, ):
        if self.user_listbox.curselection():
            user = self.user_listbox.get(self.user_listbox.curselection())[0]
            users.delete_account(user)
            self.refresh_user_list()

    def change_user(self, ):
        test_check_window.master.withdraw()
        self.master.withdraw()
        login_window.show()

    def quit(self, ):
        stop_timers()
        self.master.after(1000, root.destroy())
        sys.exit(0)

    def show_checkwindow(self, ):
        if self.randwinpos.get():
            generate_window_pos(test_check_window)
        if not test_check_window.master.winfo_viewable():
            test_check_window.master.deiconify()
        test_check_window.label_code['font'] = font.Font(size=self.entry_codefont.get())
        test_check_window.label_code['text'] = generate_code(self.entry_usesymbols.get("1.0", tk.END).strip('\n'),
                                                             self.entry_numsymbols.get())
        test_check_window.btn_ack['font'] = font.Font(size=self.entry_buttonfont.get())
        test_check_window.btn_ack['text'] = self.entry_okbuttonlabel.get()
        test_check_window.btn_late['font'] = font.Font(size=self.entry_buttonfont.get())
        test_check_window.btn_late['text'] = self.entry_latebuttonlabel.get()
        auto_window_size(test_check_window, self.entry_sizemultiplier.get())

    def update_config(self, ):
        for setting, entry in zip(list(Config.settings.items('AdminSettings')),
                                  self.admin_settings_entries):
            Config.settings.set('AdminSettings', setting[0], entry.get())
        for setting, entry in zip(list(Config.settings.items('TimeSettings')),
                                  self.time_settings_entries):
            Config.settings.set('TimeSettings', setting[0], entry.get())
        for setting, entry in zip(list(Config.settings.items('CheckWindowSettings')),
                                  self.check_windows_settings_entries):
            if setting[0] == 'usedsymbols':
                Config.settings.set('CheckWindowSettings', setting[0], entry.get(1.0, tk.END).rstrip('\n'))
            else:
                Config.settings.set('CheckWindowSettings', setting[0], entry.get())
        Config.write()
        check_window.update_settings()
        init_jobs()

    def refresh_config(self, ):
        for entry in self.admin_settings_entries:
            entry.delete(0, tk.END)
        for entry in self.time_settings_entries:
            entry.delete(0, tk.END)
        for idx, entry in enumerate(self.check_windows_settings_entries):
            if idx == 0:
                entry.delete("1.0", tk.END)
            else:
                entry.delete(0, tk.END)

        for setting, entry in zip(list(Config.settings.items('AdminSettings')),
                                  self.admin_settings_entries):
            entry.insert(tk.END, Config.read()['AdminSettings'][setting[0]])
        for setting, entry in zip(list(Config.settings.items('CheckWindowSettings')),
                                  self.check_windows_settings_entries):
            entry.insert(tk.END, Config.read()['CheckWindowSettings'][setting[0]])
        for setting, entry in zip(list(Config.settings.items('TimeSettings')),
                                  self.time_settings_entries):
            entry.insert(tk.END, Config.read()['TimeSettings'][setting[0]])

    def apply_settings(self, ):
        self.update_config()
        self.refresh_config()


def disable_event():
    pass


class LoginWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title('Вход в систему')
        w = 260
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
        self.username_label = tk.Label(self.master, text="Логин:")
        self.username_label.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

        # password
        self.password_label = tk.Label(self.master, text="Пароль:")
        self.password_label.grid(column=0, row=1, sticky=tk.E, padx=5, pady=5)

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        # login button
        self.login_button = tk.Button(self.master, text="Войти")
        self.login_button.grid(column=0, row=3, columnspan=2, sticky=tk.N, padx=5, pady=5)

        self.login_button.config(command=self.login)

    def login(self, ):
        global current_user
        login_success = False
        user = self.username_entry.get()
        password = self.password_entry.get()
        if user == 'admin':
            if password == cfg.config.read()['AdminSettings']['Password']:
                settings_window.master.deiconify()
                settings_window.master.focus_set()
                login_success = True
                current_user = 'admin'
        else:
            if users.check_password(user, password):
                login_success = True
                user_loged_in(user)
                curr_time = localtime()
                shift_start_time = strptime(cfg.config.read()['TimeSettings']['shiftstart'],
                                            "%H:%M").tm_hour * 60 + strptime(
                    cfg.config.read()['TimeSettings']['shiftstart'], "%H:%M").tm_min
                shift_end_time = strptime(cfg.config.read()['TimeSettings']['shiftend'],
                                          "%H:%M").tm_hour * 60 + strptime(
                    cfg.config.read()['TimeSettings']['shiftend'], "%H:%M").tm_min
                # print(shift_start_time)
                # print(shift_end_time)
                # print((curr_time.tm_hour * 60) + curr_time.tm_min)
                if is_in_shifttime():
                    # print(localtime())
                    # print(strptime(cfg.config.read()['TimeSettings']['shiftstart'], "%H:%M"))
                    # print('here')
                    start_control()

        if login_success:
            self.password_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.master.withdraw()

    def show(self):
        self.master.deiconify()
        self.master.focus()


def generate_appear_interval():
    intrvl = randint(int(Config.read()['TimeSettings']['MinWindowAppearInterval']) * 60,
                     int(Config.read()['TimeSettings']['MaxWindowAppearInterval']) * 60)
    print(intrvl)
    print((datetime.now() + timedelta(seconds=intrvl)))
    return intrvl


def is_in_shifttime():
    curr_time = localtime()
    shift_start_time = strptime(cfg.config.read()['TimeSettings']['shiftstart'],
                                "%H:%M").tm_hour * 60 + strptime(
        cfg.config.read()['TimeSettings']['shiftstart'], "%H:%M").tm_min
    shift_end_time = strptime(cfg.config.read()['TimeSettings']['shiftend'],
                              "%H:%M").tm_hour * 60 + strptime(
        cfg.config.read()['TimeSettings']['shiftend'], "%H:%M").tm_min
    if shift_end_time > shift_start_time:
        return True if shift_end_time > (curr_time.tm_hour * 60) + curr_time.tm_min > shift_start_time else False
    else:
        return True if shift_end_time < (curr_time.tm_hour * 60) + curr_time.tm_min \
                       or shift_start_time > (curr_time.tm_hour * 60) + curr_time.tm_min else False


def generate_window_pos(window):
    auto_window_size(window, Config.read()['CheckWindowSettings']['SizeMultiplier'])
    rand_display_num = randint(1, len(monitors)) - 1
    bottom_border = monitors[rand_display_num].height - checkwindow_height
    right_border = monitors[rand_display_num].width - checkwindow_width
    [monitor_x, monitor_y] = [monitors[rand_display_num].x, monitors[rand_display_num].y]
    windset_pos_x = randint(monitor_x, monitor_x + right_border)
    windset_pos_y = randint(monitor_y, monitor_y + bottom_border)
    window.master.geometry('+%d+%d' % (windset_pos_x, windset_pos_y))
    # print('Window_x:', windset_pos_x, 'Window_y:', windset_pos_y, 'Monitor_x:', monitor_x, 'Monitor_y:', monitor_y)
    window.window_appeared_at = datetime.now()
    window.label_code['text'] = generate_code(Config.read()['CheckWindowSettings']['usedsymbols'],
                                              Config.read()['CheckWindowSettings']['codelength'])
    window.master.deiconify()


def start_reveal_timer():
    global generate_timer
    generate_timer = RepeatableTimer(generate_appear_interval(), generate_win_pos_and_timer, [])
    generate_timer.start()


def start_miss_timer():
    global timer_missed
    timer_missed = RepeatableTimer(int(Config.read()['TimeSettings']['WindowAppearDuration']), confirmation_missed, [])
    if not timer_missed._interval == 0:
        timer_missed.start()


def generate_win_pos_and_timer():
    generate_window_pos(check_window)
    start_miss_timer()


def confirmation_missed():
    if check_window.master.winfo_viewable():
        time_miss = datetime.now() - check_window.window_appeared_at
        window_appeared_at_time = check_window.window_appeared_at.strftime('%H:%M')
        logg.logging.info('Не квитировано !!! (время появления:%s),(прошло времени:%s)', window_appeared_at_time,
                          time_miss)
        check_window.master.withdraw()
        start_reveal_timer()


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

# timer_missed=Timer(3.0, confirmation_missed)
class RepeatableTimer(object):
    def __init__(self, interval, function, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.t = Timer(self._interval, self._function, *self._args, **self._kwargs)

    def start(self):
        self.t.start()
        # print('started',self._interval)

    def cancel(self):
        self.t.cancel()


def auto_window_size(window, multiplier):
    global checkwindow_height
    global checkwindow_width
    min_display_height = min(m.height for m in monitors)
    min_display_width = min(m.width for m in monitors)
    checkwindow_height = int(min_display_height * float(multiplier))
    checkwindow_width = int(min_display_width * float(multiplier))
    window.master.geometry('%dx%d' % (checkwindow_width, checkwindow_height))


# ОЧЕНЬ ПЛОХО???
def listener_thread():
    def on_activate():
        global current_user
        if current_user != 'admin':
            stop_timers()
            user_loged_out()
            check_window.master.withdraw()
            login_window.show()
            login_window.master.focus()
            login_window.master.attributes('-topmost', True)

    def for_canonical(f):
        return lambda k: f(what.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+]'),
        on_activate)

    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as what:
        what.join()


def stop_timers():
    # global timer_missed
    # global generate_timer
    generate_timer.cancel()
    timer_missed.cancel()


def user_loged_in(user):
    global current_user
    current_user = user
    logg.logging.info('%s Пользователь %s вошел в систему',
                      datetime.now().strftime('%H:%M:%S'),
                      current_user)


def user_loged_out():
    global current_user
    logg.logging.info('%s Пользователь %s вышел из системы',
                      datetime.now().strftime('%H:%M:%S'),
                      current_user)
    current_user = None


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


#########################################################################

def test_checkwindow_settings():
    test_check_window.master.title('Пример проверочного окна')
    test_check_window.master.withdraw()
    test_check_window.master.resizable(0, 0)
    test_check_window.master.attributes('-toolwindow', True)
    test_check_window.master.geometry('+%d+%d' % (int(root.winfo_screenwidth() / 2),
                                                  int(root.winfo_screenheight() / 2)))
    test_check_window.btn_ack.config(command=disable_event)
    test_check_window.btn_late.config(command=disable_event)
    test_check_window.master.protocol("WM_DELETE_WINDOW", test_check_window.master.withdraw)
    test_check_window.master.overrideredirect(0)
    test_check_window.master.wm_attributes("-topmost", True)


root = tk.Tk()
Config = cfg.config
monitors = get_monitors()
current_user = None

checkwindow_height = 200
checkwindow_width = 300

timer_missed = RepeatableTimer(int(Config.read()['TimeSettings']['WindowAppearDuration']), confirmation_missed, ())
generate_timer = RepeatableTimer(None, generate_win_pos_and_timer, ())

key_listener_thread = Thread(target=listener_thread, )
key_listener_thread.daemon = True
key_listener_thread.start()

settings_window = SettingsWindow(root)
login_window = LoginWindow(root)
check_window = CheckWindow(root)
test_check_window = CheckWindow(root)

test_checkwindow_settings()

settings_window.master.withdraw()
check_window.master.withdraw()

# auto_window_size(check_window)
# generate_win_pos_and_timer()

root.withdraw()
root.mainloop()
