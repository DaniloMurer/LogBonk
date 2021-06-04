import string

import schedule
import threading

"""
Method is being called by scheduler with one config file
:param config_file Config File path for the cron_job_task
"""
def cron_job_task(config_file: string):
    print(config_file)


def cron_job():
    print("I'm starting the cronjobtask")
    for i in range(10):
        thread = threading.Thread(target=cron_job_task, args=("test",))
        thread.start()


schedule.every(1).minutes.do(cron_job)

while True:
    schedule.run_pending()


