import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.header    import Header
from email import encoders
import datetime as dt
import time
import logg
import cfg
import os


def send_mail(send_from, send_to, subject, message, files=[],
              server="", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    # msg['Subject'] = subject
    msg['Subject'] = Header(subject, 'utf-8')
    # msg.add_header('Subject', subject)

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    # try:
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    # except smtp.SMTPResponseException as e:
    #     error_code = e.smtp_code
    #     error_message = e.smtp_error
    #     print(error_code, error_message)


def send_day_report():
    send_mail(send_from=cfg.config.read()['AdminSettings']['Email'],
              send_to=cfg.config.read()['AdminSettings']['Emails'],
              subject=f'Контроль оператора: Отчет за {dt.date.today() - dt.timedelta(days=1)}',
              message='',
              files=[logg.LOG_FILE],
              server=cfg.config.read()['AdminSettings']['SmtpServer'],
              port=cfg.config.read()['AdminSettings']['EmailPort'],
              username=cfg.config.read()['AdminSettings']['Email'],
              password=cfg.config.read()['AdminSettings']['EmailPassword'],
              use_tls=True)


def send_month_report():
    create_month_report()
    send_mail(send_from=cfg.config.read()['AdminSettings']['Email'],
              send_to=cfg.config.read()['AdminSettings']['Emails'],
              # TODO: исправить на месяц
              subject=f'Контроль оператора: Отчет за {dt.date.today() - dt.timedelta(days=1)}',
              message='',
              files=[logg.month_log_folder + "/" + (
                          dt.datetime.fromtimestamp(time.time()) - dt.timedelta(days=1)).strftime('%Y_%m') + ".log"],
              server=cfg.config.read()['AdminSettings']['SmtpServer'],
              port=cfg.config.read()['AdminSettings']['EmailPort'],
              username=cfg.config.read()['AdminSettings']['Email'],
              password=cfg.config.read()['AdminSettings']['EmailPassword'],
              use_tls=True)
    pass


def create_month_report():
    outf = logg.month_log_folder + "/" + (dt.datetime.fromtimestamp(time.time()) - dt.timedelta(days=1)).strftime(
        '%Y_%m') + ".log"
    with open(outf, "wb") as outfile:
        for f in os.listdir(logg.month_log_folder):
            filename = logg.month_log_folder + "/" + f
            with open(filename, "rb") as infile:
                outfile.write(infile.read())


def send_report():
    send_day_report()
    if dt.date.today().day == 1:
        send_month_report()
    logg.configure_day_log()
