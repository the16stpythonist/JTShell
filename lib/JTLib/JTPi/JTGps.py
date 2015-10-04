# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:47:37 2015
@author: Jonas
###
The module to contain basic functionality for using gpsd compatible antennas
with the Raspberry Pi.
Before using this module make sure you have installed the necessary packages
on the raspberry pi, which would be automaticly installed issueing the command:
"sudo apt-get install gpsd gpsd-clients python-gps" and
"sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock"
Module is designed to interact with the "GlobalSat BU-353 USB GPS Receiver"
"""
import threading
import serial

class Gps(threading.Thread):
    """
    A class, which is basically wrapping the data output offered by any compatible USB Gps receiver, that is connected
    to the raspberry pi, making the data easily accessible by steadily updating the object properties according to the
    standard protocol output stream of the gps receiver. Because this is a very basic implementation of such
    functionality, the Thread is not only consuming quit a bit of processing capacity, but is also a whole lot slower
    than the origninal reciever, as the class is utilizing a slow serial uart connection to completely read the stream
    of the gps output to fetch the full protocol, which wouldnt be possible, when using the default python io streams.
    To function properly the object needs the string path of the stream location passed as an argument, which will most
    likely be a tty*** type of file in the /var folder
    :parameter stream: (string) the path to the output stream of the gps to be used
    :var latitude: (string) the latitude of the gps in the format "angle°minutes'"
    :var longitude: (string) the longitude of the gps in the format "angle°minutes'"
    :var altitude: (string) the height above sea level
    :var time: (string) the accurate gps clock in the format "hh:mm:ss"
    :var running: (bool) the control variable for the thread
    """
    def __init__(self, stream):
        # initializing the Thread
        threading.Thread.__init__(self)
        self.file = stream
        # creating the gpsd relevant attribute
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.speed = 0
        self.time = ""
        self.date = ""
        self.satellites = 0
        self.running = False
        
    def run(self):
        """
        the main loop of the Thread, that only has the simple task to update 
        the next set of data into an internal buffer to be read
        ###
        RETURNS (void)
        """
        self.running = True
        # the temporary list of lines, read from the input stream
        temp_line = []
        # opening the serial connection with the usb gps dongle as the uart protocol object
        uart = serial.Serial(self.file, 4800)
        uart.open()
        while self.running:

            # reading the first transmitted character, in case this is the start character "$", it'll go on
            # with checking whether it is the right protocol or not
            character = uart.read()
            if str(character) is "$":
                string = ""
                for counter in range(4):
                    character = uart.read()
                    string = string + str(character)
                # in case the right protocol has been detected the program goes on and reads the whole string
                if "GPGG" in str(string):
                    # reading the characters until the line has been ended by the "\n" linebreak character
                    while str(character) != "\n":
                        character = uart.read()
                        string = string + str(character)
                    # removing the newline character from the string
                    string = string.replace("\r\n", "")
                    # splitting the string into a data list separated by the kommata within
                    datalist = string.split(",")
                    self._update_time(datalist[1])
                    self._update_latitude(datalist[2], datalist[3])
                    self._update_longitude(datalist[4], datalist[5])
                    self._update_altitude(datalist[9], datalist[10])

    def _update_time(self, raw_time):
        """
        a method to update the time variable of the Gps object, when passed the raw time integer of the gps output
        :param raw_time: (int) the raw integer given by the output stream
        :return: (void)
        """
        self.time = str(raw_time)[0:2] + ":" + str(raw_time)[2:4] + ":" + str(raw_time)[4:6]

    def _update_latitude(self, degrees, direction):
        """
        a method to update the latitude variable, when given the raw string of degrees and the reference direction
        :param degrees: (str) the raw string of degrees obtained by the output stream
        :param direction: (char) the direction, either north or south
        :return: (void)
        """
        self.latitude = str(degrees)[0:2] + "°" + str(degrees)[2:-1] + "' " + str(direction)

    def _update_longitude(self, degrees, direction):
        """
        a method to update the latitude variable, when given the raw string of degrees and the reference direction
        :param degrees: (str) the raw string of degrees obtained by the output stream
        :param direction: (char) the direction, either ost ort west
        :return: (void)
        """
        self.longitude = str(degrees)[0:2] + "°" + str(degrees)[2:-1] + "' " + str(direction)

    def _update_altitude(self, value, unit):
        """
        a method to update the altitude variable, when given the raw value and the unit in which the value is meassured
        :param value: (int) the value of the altitude
        :param unit: (str) the corresponding unit of the value, whether its meters or kilometers
        :return: (void)
        """
        self.altitude = str(value) + " " + str(unit)

    def stop(self):
        """
        stops the Thread, by calling the _stop method of the Thread-superclass
        :return: (bool) whether the Thread has successfully been stopped or not
        """
        self._stop()
        if self._is_stopped:
            return True
        else:
            return False
        
