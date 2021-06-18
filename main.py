import string
import tkinter as tk
from datetime import datetime
from ftplib import FTP
import os


def send_file_to_server():
    print("sending file over ftp")

    config_file_path = generate_config_file(configMailToField.get(), configKeywordField.get(),
                                            configLogsPathField.get(), configLogsArchivePath.get())
    with FTP(ftpServerField.get()) as ftp:
        ftp.login(user=ftpUsernameField.get(), passwd=ftpPasswordField.get())
        ftp.cwd("/app/data/config")
        ftp.storbinary('STOR ' + config_file_path, open(config_file_path, 'rb'))
        ftp.quit()
    os.remove(config_file_path)


def generate_config_file(mailto, keywords, logs_path, logs_archive):
    print("generating config file....")
    # Weird format because else there is a tab at the beginning of every line
    config_file_content = """
[Logging Configuration]
keyword={}
logs.path={}
logs.archive.path={}
[Mail Configuration]
mail.to={}
    """.format(keywords, logs_path, logs_archive, mailto)
    config_file_name = "config_{}.ini".format(datetime.now().date())
    config_file = open(config_file_name, "w")
    config_file.write(config_file_content)
    config_file.close()
    return config_file_name


master = tk.Tk()

tk.Label(master, text="FTP Username").grid(row=0)
tk.Label(master, text="FTP Password").grid(row=1)
tk.Label(master, text="FTP Server").grid(row=2)
tk.Label(master, text="Mail To").grid(row=3)
tk.Label(master, text="Keywords").grid(row=4)
tk.Label(master, text="Logs Path").grid(row=5)
tk.Label(master, text="Logs Archive Path").grid(row=6)

ftpUsernameField = tk.Entry(master)
ftpPasswordField = tk.Entry(master, show="*")
ftpServerField = tk.Entry(master)

ftpUsernameField.grid(row=0, column=1)
ftpPasswordField.grid(row=1, column=1)
ftpServerField.grid(row=2, column=1)

configMailToField = tk.Entry(master)
configKeywordField = tk.Entry(master)
configLogsPathField = tk.Entry(master)
configLogsArchivePath = tk.Entry(master)

tk.Button(master, text="Quit", command=master.quit).grid(row=7, column=0, sticky=tk.W, pady=4)
tk.Button(master, text="Send Config File", command=send_file_to_server).grid(row=7, column=1, sticky=tk.W, pady=4)

configMailToField.grid(row=3, column=1)
configKeywordField.grid(row=4, column=1)
configLogsPathField.grid(row=5, column=1)
configLogsArchivePath.grid(row=6, column=1)

configKeywordField.grid()

master.mainloop()
