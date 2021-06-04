import string

import schedule
import threading
import configparser

"""
Method is being called by scheduler with one config file
:param config_file Config File path for the cron_job_task
"""
def cron_job_task(config_file: string):
    print(config_file)
    config = configparser.ConfigParser()
    config.read(config_file)

    log_file = config["Logging Configuration"]["logs.path"]
    keywords = str(config["Logging Configuration"]["keyword"]).split(";")

    file = open(log_file, "r")
    lines = file.readlines()

    for line in lines:
        for keyword in keywords:
            if keyword in line:
                print("KEYWORD FOUND")
                # send email

def cron_job():
    print("I'm starting the cronjobtask")

    # Get all available log files
    for i in range(10):
        thread = threading.Thread(target=cron_job_task, args=("../sample/config.ini",))
        thread.start()


schedule.every(1).minutes.do(cron_job)

while True:
    schedule.run_pending()


