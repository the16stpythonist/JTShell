__author__ = 'Jonas'
import time
import os
from JTLib.JTOS.JTCombinedOs import createfile


class Logger:

    def __init__(self):
        # creating the file object within the cwd, which is originally the main Shell folder, thus the log has to be
        # placed within the sub folder "log"
        self.filepath = os.getcwd() + "\\log\\"
        # creating the filename with the date
        self.filename = time.strftime("%Y_%m_%d") + ".slog"
        if os.path.exists(self.filepath + self.filename):
            # in case there already was an open session that day and there already exists a log file for the current
            # date, simply opens that up and transfers the already written content to the new file object
            temporary_file = open(self.filepath + self.filename, "r")
            previous_content = temporary_file.read()+"\n"
            self.file = open(self.filepath + self.filename)
            self.file.write(previous_content)
        else:
            # if there isn#t already an file, goes on and creates one
            createfile(self.filepath + self.filename)
            self.file = open(self.filepath + self.filename)

    def write(self):
        pass