import configparser, os
import string

path = 'settings.ini'


def create_default_config(path):
    """
    Create a config file
    """
    settings = configparser.ConfigParser(allow_no_value=True)
    settings['TimeSettings'] = {
        "ShiftStart": "9:30",  # Начало смены
        "ShiftEnd": "7:30",  # Конец смены
        "ReportSendTime": "8:00",  # Время отправки отчета
        "MinWindowAppearInterval": '15',  # (минуты) Минимальное время появления окна
        "MaxWindowAppearInterval": '60',  # (минуты) Максимальное время появления окна
        "WindowAppearDuration": '0',  # (секунды) Длительность отображения окна
        "NeedReactionTime": '120'  # (секунды) Необходимое время реакции оператора
    }
    settings['CheckWindowSettings'] = {
        "CodeLength": "4",  # Длина кода
        "UsedSymbols": (string.digits + string.ascii_lowercase + string.ascii_uppercase + \
                        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),
        # Используемые символы
        "CodeFont": '60',  # Размер шрифта кода
        "OkBtnLabel": 'Ок',  # Надпись на кнопке 1
        "LateBtnLabel": 'Был на обходе',  # Надпись на кнопке 2
        "BtnFont": '20',  # Размер шрифта на кнопках
        "SizeMultiplier": "0.2",  # Длина кода
    }
    settings['ReportSettings'] = {
        "Emails": "",  # Список emailов для рассылки
        "LateReactMsg": "!!!",  # Запись при превышении времени реакции
        "NoReactMsg": "---",  # Запись при осутствии реакции
        "Delimiter": "*"  # Разделитель
    }
    settings['AdminSettings'] = {
        "Password": "admin"  # пароль админа
    }
    # Временные уставки
    # settings.add_section("TimeSettings")
    # settings.set("TimeSettings", "ShiftStart", "9:30")  # Начало смены
    # settings.set("TimeSettings", "ShiftEnd", "7:30")  # Конец смены
    # settings.set("TimeSettings", "ReportSendTime", "8:00")  # Время отправки отчета
    # settings.set("TimeSettings", "MinWindowAppearInterval", '15')  # (минуты) Минимальное время появления окна
    # settings.set("TimeSettings", "MaxWindowAppearInterval", '60')  # (минуты) Максимальное время появления окна
    # settings.set("TimeSettings", "WindowAppearDuration", '0')  # (секунды) Длительность отображения окна
    # settings.set("TimeSettings", "NeedReactionTime", '120')  # (секунды) Необходимое время реакции оператора
    # Окно проверки
    # settings.add_section("CheckWindowSettings")
    # settings.set("CheckWindowSettings", "CodeLength", "4")  # Длина кода
    # codesymbols = string.digits + string.ascii_lowercase + string.ascii_uppercase + \
    #               'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    # settings.set("CheckWindowSettings", "UsedSymbols", codesymbols)  # Используемые символы
    # settings.set("CheckWindowSettings", "CodeFont", '60')  # Размер шрифта кода
    # settings.set("CheckWindowSettings", "OkBtnLabel", 'Ок')  # Надпись на кнопке 1
    # settings.set("CheckWindowSettings", "LateBtnLabel", 'Был на обходе')  # Надпись на кнопке 2
    # settings.set("CheckWindowSettings", "BtnFont", '20')  # Размер шрифта на кнопках
    # settings.set("CheckWindowSettings", "SizeMultiplier", "0.2")  # Длина кода
    # Отчет
    # settings.add_section("ReportSettings")
    # settings.set("ReportSettings", "Emails", "")  # Список emailов для рассылки
    # settings.set("ReportSettings", "LateReactMsg", "!!!")  # Запись при превышении времени реакции
    # settings.set("ReportSettings", "NoReactMsg", "---")  # Запись при осутствии реакции
    # settings.set("ReportSettings", "Delimiter", "*")  # Разделитель
    # Пароль админа
    # settings.add_section("AdminSettings")
    # settings.set("AdminSettings", "Password", "admin")  # пароль админа

    with open(path, "w") as config_file:
        settings.write(config_file)


def read_config():
    settings = configparser.ConfigParser()
    settings.read(path)
    return settings


class Config:
    def __init__(self):
        self.settings = configparser.ConfigParser()

    def create_default(self, ):
        """
        Create a config file
        """
        settings = configparser.ConfigParser(allow_no_value=True)
        settings['TimeSettings'] = {
            "ShiftStart": "09:30",  # Начало смены
            "ShiftEnd": "07:30",  # Конец смены
            "ReportSendTime": "08:00",  # Время отправки отчета
            "MinWindowAppearInterval": '15',  # (минуты) Минимальное время появления окна
            "MaxWindowAppearInterval": '60',  # (минуты) Максимальное время появления окна
            "WindowAppearDuration": '0',  # (секунды) Длительность отображения окна
            "NeedReactionTime": '120'  # (секунды) Необходимое время реакции оператора
        }
        settings['CheckWindowSettings'] = {
            "CodeLength": "4",  # Длина кода
            "UsedSymbols": (string.digits + string.ascii_lowercase + string.ascii_uppercase + \
                            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),
            # Используемые символы
            "CodeFont": '60',  # Размер шрифта кода
            "okbuttonlabel": 'Ок',  # Надпись на кнопке 1
            "latebuttonlabel": 'Был на обходе',  # Надпись на кнопке 2
            "BtnFont": '20',  # Размер шрифта на кнопках
            "SizeMultiplier": "0.2",  # Длина кода
        }
        settings['ReportSettings'] = {
            "Emails": "",  # Список emailов для рассылки
            "LateReactMsg": "!!!",  # Запись при превышении времени реакции
            "NoReactMsg": "---",  # Запись при осутствии реакции
            "Delimiter": "*"  # Разделитель
        }
        settings['AdminSettings'] = {
            "Password": "admin",  # пароль админа
            "Email": "",
            "EmailPassword": "",
            "EmailPort": "587",
        }

        with open(path, "w") as config_file:
            settings.write(config_file)

    def write(self):
        with open(path, "w") as config_file:
            self.settings.write(config_file)

    def read(self):
        self.settings.read(path)
        return self.settings


TimeSettingsLabels = {
    "Начало смены",
    "Конец смены",
    "Время отправки отчета",
    "Минимальное время появления окна (минуты)",
    "Максимальное время появления окна (минуты)",
    "Длительность отображения окна (секунды)",
    "Необходимое время реакции оператора (секунды)"
}

config = Config()
if not os.path.exists(path):
    config.create_default()
