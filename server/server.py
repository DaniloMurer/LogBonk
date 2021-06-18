import string

import schedule
import threading
import configparser
import os
import shutil
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email_config


def send_mail(address, content):
    """
    Method for sending an E-Mail passing content and To: Address

    :param address: E-Mail Address to send the Mail to
    :param content: Content of the E-Mail
    :return: nothing
    """
    # send email
    print("Sending E-Mail")
    with smtplib.SMTP(host=email_config.smtp_server, port=email_config.smtp_port) as smtp_server:
        smtp_server.connect(host=email_config.smtp_server, port=email_config.smtp_port)
        smtp_server.starttls()
        smtp_server.login(email_config.smtp_username, email_config.smtp_password)
        message = MIMEMultipart("alternative")
        message["Subject"] = "LogBonk Alert"
        message["To"] = address
        message["From"] = email_config.smtp_username
        message.attach(MIMEText(content, "plain"))
        smtp_server.sendmail(email_config.smtp_username, address, message.as_string())


def cron_job_task(config_file: string):
    """
    Method called by cron_job() passing a log file as parameter

    :param config_file: Path to the configfile which is used for the task
    :return: nothing
    """

    # Read Config file
    config = configparser.ConfigParser()
    config.read(config_file)
    log_files_path = str(config["Logging Configuration"]["logs.path"])
    log_files = os.listdir(log_files_path)
    archive_path = str(config["Logging Configuration"]["logs.archive.path"])
    keywords = str(config["Logging Configuration"]["keyword"]).split(";")
    email = str(config["Mail Configuration"]["mail.to"])

    for log_file in log_files:
        if '.log' in log_file:
            fqfn = log_files_path + '/' + log_file

            file = open(fqfn, "r")
            lines = file.readlines()

            # Check for keyword in log files
            for line in lines:
                for keyword in keywords:
                    if keyword in line:
                        # send email
                        send_mail(email, line)

            file.close()
            print("Moving files")
            # Move logs to archive folder
            shutil.move(fqfn, archive_path + '/' + log_file)

    # Check Archive logs
    log_files_archive = os.listdir(archive_path)
    for log_file_archive in log_files_archive:
        fqafn = archive_path + '/' + log_file_archive

        if datetime.fromtimestamp(os.path.getctime(fqafn)) <= (datetime.now() - timedelta(days=30)):
            os.remove(fqafn)


def cron_job():
    """
    Method called by scheduler which start new threads for cronjob tasks based
    on the config files found

    :return: nothing
    """
    print("I'm starting the cronjobtask")

    # Get all available log files
    # thread = threading.Thread(target=cron_job_task, args=("../sample/config.ini",))
    # thread.start()
    config_files = os.listdir("/app/data/config")
    for config_file in config_files:
        if ".ini" in config_file:
            fqcn = "/app/data/config/" + config_file
            cron_job_task(fqcn)


schedule.every(5).seconds.do(cron_job)

while True:
    schedule.run_pending()
