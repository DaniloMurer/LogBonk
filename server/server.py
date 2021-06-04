import string

import schedule
import threading
import configparser
import os
import shutil
from datetime import datetime, timedelta

"""
Method is being called by scheduler with one config file
:param config_file Config File path for the cron_job_task
"""
def cron_job_task(config_file: string):
    print(config_file)
    config = configparser.ConfigParser()
    config.read(config_file)
    log_files_path = config["Logging Configuration"]["logs.path"]
    log_files = os.listdir(log_files_path)
    archive_path = config["Logging Configuration"]["logs.archive.path"]
    keywords = str(config["Logging Configuration"]["keyword"]).split(";")

    for log_file in log_files:
        if '.log' in log_file:
            fqfn = log_files_path + '\\' + log_file
            file = open(fqfn, "r")
            lines = file.readlines()

            # Check for keyword in log files
            for line in lines:
                for keyword in keywords:
                    if keyword in line:
                        print("KEYWORD FOUND")
                        # send email

            # Move logs to archive folder

            shutil.move(fqfn, archive_path + '\\' + log_file)
            #if datetime.fromtimestamp(os.path.getctime(log_file)) == datetime.now() + timedelta(hours=)

def cron_job():
    print("I'm starting the cronjobtask")

    # Get all available log files
    #thread = threading.Thread(target=cron_job_task, args=("../sample/config.ini",))
    #thread.start()

    cron_job_task("../sample/config.ini")


schedule.every(5).seconds.do(cron_job)

while True:
    schedule.run_pending()


