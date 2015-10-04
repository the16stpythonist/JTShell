# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:47:19 2015
@author: Jonas
###
A package containing the relavant Software applications for the Schiller in Space
onboard RaspberryPi. the main program is build as a multithreaded combination of 
single sensors or sensor arrays. the program consists of a DataExchange object
and the Threads for the sensors, a console thread, a timing thread and a 
logging thread. the status of the threads is determined by an locked exchanged 
status variable, which can be accesed by every thread, as there may be several
sensors being permitted to conduct a system exit.
TODO:
- extended Eventlog showing certain important stages of Threads/Sensors
- extend TestThread
    - showing the eventlog
- making the Logging Thread save parts of the documents after certain amounts
  of time to prevent data loss
"""
import JTLib.JTFiles.JTTextfiles as jtfiles
import JTLib.JTPi.JTGps as jtgps
import JTLib.JTPi.JTGpio as gpio
import JTLib.JTOS.JTLinux as jtos
import threading
import os
import time
import serial

"""
the DataExchange object specificly designed for the schiller in space purposes
therefor managing the programstate. The sensors are virually infinitly expandable
due to the management with an dictionary and a registration function, which has to
be called by every new sensor thread to appear in the logfile
"""
class DataExchange():
    """
    programstate - (bool) the state of the overall program, including the threads
                          as this is the variable, that conditions the system exit
    programstate_lock - (Lock) the Lock of the programstate variable
    loglist - (list/string) the list with the subjects, that are to be logged
    data - (dict/string-int) the main dictionary of the ExchnageObject storing the
                             sensor name and the corresponding data value of the sensor
    """
    def __init__(self):
        # setting up the class variables 
        self.programstate = True
        self.programstate_lock = threading.Lock()
        # setting up the data dictionary
        self.data = {}
        # setting up the textfile inheriting the status log of the file
        self.eventlog = jtfiles.SimpleFile("/home/pi/slog.txt", False, False)
        self.eventlog_lock = threading.Lock()
        self.log("The Eventlog of the Schiller in Space flight")
        
    def set_programstate(self, state):
        """
        sets the programstate most likly to false, but could also be used to set 
        it as true
        ###
        state - (bool) the new state of the program
        ###
        RETURNS (void)
        """
        self.programstate_lock.acquire()
        self.programstate = state
        self.programstate_lock.release()
        
    def set_data(self, name, value):
        """
        sets the data of the sensor with the given name to the new value
        ###
        value - (int) the new value of the specified sensor 
        ###
        RETURNS (void)
        """
        if name in self.data.keys():
            self.data[name] = value

    def log(self, content):
        """
        logs the passed string content to the predefined logfile
        ###
        content - (string) the string to be logged into the file
        ###
        RETURNS (void)
        """
        self.eventlog_lock.acquire()
        self.eventlog.writeln(content)
        self.eventlog_lock.release()
    
    def register_sensor(self, name, initial=0):
        """
        adds a new sensor to the DataExchnage object, which means defining a new 
        name plus value data pair to the internal dictionary, which then can be accesed.
        This should be called within the constructor
        of every Sesnor thread, so that it can be accesed by the logfile thread
        ###
        name - (string) the name wich will then later be one of the subjects of 
                        of the logging file
        ###
        RETURNS (void)
        """
        self.data[name] = initial        
        
    def __iter__(self):
        """
        returns the the tuple list (key, value) of the internal dictionary to
        iter through
        ###
        RETURNS (list/tuple/str-int)
        """
        return self.data.items()
        
    def __len__(self):
        """
        returns the amount of sensors registerd in the DataExchange object
        ###
        RETURNS (int)
        """
        return len(self.data)
        
    def __getitem__(self, key):
        """
        returns the temporary data, whenever given the sensor name
        ###
        RETURNS (int)
        """
        return self.data[key]
  
"""
the baseclass for all Schiller in Space threads, mainly functioning as an 
an interface to make sure objects are inhereting the core variables, being 
the dataexchange object connecting every Thread to the main Logging Thread,
saving the Data in one main file
###
dataexchange - (DataExchange) the exchange object
"""
class SiSThread(threading.Thread):
    """
    exchange - (DataExchange) the exchange object
    """
    def __init__(self, dataexchange):
        threading.Thread.__init__(self)
        self.exchange = dataexchange
        
      
"""
the Thread managing the Geiger counter and updating the geiger value within the
DataExcahnge object. It has to be mentioned, that this will mostlikely have an
upper borde of how many counts per second this can register, depending on the
processing power of the unit running this script.
Also the used SparkFun GeigerCounters have to be calibrated in order to function
properly, because the tested devices all seem to have a logarithmic behaviour
similar to any industrial GeigerCounter, butall seem to count different amounts
of ticks, therefor the parameter factor is the integer value of the calibrated
correction factor.
###
dataexchange - (DataExchange) the exchange object
pin - (int) the index of the RaspPi Gpio pin
interval - (~int) the interval in seconds in which the value of the geiger counter
                  gets updated. 30 seconds on default 
name - (string) the name of the Thread 
factor - (int) the calibrated correction factor, every tick count to be multiplied
               with
"""
class GeigerThread(SiSThread):
    """
    exchange - (DataExchange) the exchange object
    interval - (int) the predefined interval in which the new value of the geiger
                     counter is updated
    port - (GpioInput) the JTGpio GpioInput object managing the hardwar side 
                       of the meassuring process. is accessed wether an count 
                       occured or not.
    count - (int) the temporary number of counts meassured, renewed every interval
    name - (string) the name of the Thread 
    """
    def __init__(self, dataexchange, pin, interval=30, name="GeigerCounter", factor=5.5):
        SiSThread.__init__(self, dataexchange)
        self.name = name
        self.exchange.register_sensor(self.name)
        self.interval = 30
        gpio.setup("Pin")
        self.port = gpio.InputGpio(pin)
        self.count = 0
        self.factor = factor
        # logging
        
    def run(self):
        """
        the threading main loop in dependency of the exchanged programstate variable.
        counts the ticks with a switch condition, meaning a count will only be 
        recongnized as such when the value switches from High to Low.
        ###
        RETURNS (void)
        """
        self.exchange.log("[+] running Geiger Thread")
        # main loop with exchanged programstate condition
        t_start = time.time()
        # condition to add a count. will only add a count, if there has been a change
        # in value, meianing whenever the previous value was 0 and the claue then changed
        # to True
        prev_value = 0
        try:
            while self.exchange.programstate:
                # the time difference, later being checked with the interval variable
                t_delta = time.time() - t_start
                if self.port.get_state() == 1 and prev_value == 0:
                    prev_value = 1
                elif self.port.get_state() == 0 and prev_value == 1:
                    prev_value = 0
                    self.count += 1
                if t_delta >= self.interval:
                    # udpadating the exchanged geiger value and resetting the count variable
                    self._update_data()
                    t_start = time.time()
        finally:
            self.exchange.log("[*] terminated Geiger Thread")
            gpio.cleanup()
                
        
    def _update_data(self):
        """
        simply calls the set_geiger method of the exchange object with the current
        counted class variable 'self.count' and afterwards resets said variable
        ###
        RETURNS (void)
        """
        self.exchange.set_data(self.name, int(self.count*self.factor))
        self.count = 0

        
"""
The Thread managing microsoft Excel compatible logfile, in the first line listing
the names of the registered sensors and then the values of the sensors seperated
only by semicolons, so that the file can directly be translated into a excel file
###
dataexchange - (DataExchange) the exchange object
filepath - (string) the absolute path of the file to write the log into
interval - (~int) the interval in whcih the new data i sbeing written into an 
                  new row of the logfile. 2 seconds on default
"""
class LogThread(SiSThread):
    """
    logfile - (ExcelLogfile) the JTFiles ExcelLogfile object managing the file
                             to write the log in. Providing simple functions for
                             logging applications
    path - (string) the absolute path of the file to write the log into
    t_total - (int) the total amount of time in seconds, that has passed since 
                    the beginning of the program
    interval - (int) the amount of time in seconds, that is between two rows of 
                     new data
    """
    def __init__(self, dataexchange, folderpath, interval=2):
        SiSThread.__init__(self, dataexchange)
        # the logfile expects an specific subjects argument wich is the loglist
        # class variable of the DataExchange object and this may not be complete
        # at the time of construction, but rather the actual start of the thread
        self.logfile = None
        self.interval = interval
        self.src_path = folderpath
        self.t_total = 0
        self.index = 0
        self.exchange.log("[+] created Log Thread")
        
    def run(self):
        """
        the threading main loop in dependency of the exchanged programstate variable.
        calling the data dictionary of the DataExchange for values as well as keys
        to write the subjects and the corresponding values into the logfile 
        ###
        RETURNS (void)
        """
        self.exchange.log("[+] running Log Thread")
        # creating the logfile, as every sensor is registered by now 
        jtos.createfile(self.src_path+"/log"+str(self.index))
        self.logfile = jtfiles.ExcelLogfile(self.src_path+"/log"+str(self.index), ["time"]+list(self.exchange.data.keys()), overwrite=False)
        # main loop with exchanged programstate condition
        t_start = time.time()
        once = True
        try:
            while self.exchange.programstate:
                t_delta = time.time() - t_start
                if t_delta >= self.interval:
                    self.t_total += t_delta
                    once = True
                    self.logfile.writelog([int(self.t_total)]+list(self.exchange.data.values()))
                    t_start = time.time()
                if int(self.t_total) in range(60,6000000,60) and once == True:
                    self.logfile.end()
                    self.index += 1
                    jtos.createfile(self.src_path+"/log"+str(self.index))
                    self.logfile = jtfiles.ExcelLogfile(self.src_path+"/log"+str(self.index), ["time"]+list(self.exchange.data.keys()), overwrite=False) 
                    once = False
        finally:
            self.logfile.end()
            self.exchange.log("[*] terminated Log thread")
        
"""
the thread managing the Digital Temperature Sensors DS1820, which are connected
to the raspberry pi via the unique one wire bus system, that is also supported
by the Raspberry Pi on default.
When using the Temperature Thread, it will automaticly manage every properly
connected device on its own, not having to rely on passing the Thread the Pin,
on which the device is connected, as this functionality is already included in
the Pi's own implementation, that consists of creating a special directory for
each connected sensor, in which the data is continuesly updated to the "w1_slave"
file inside of it.
NOTE:
When working with an RespberryPi B+/B2 make sure to write the additional line
'btoverlay=w1-gpio' into the file '/boot/config.txt'
###
dataexchange - (DataExchange) the exchange object
interval - (int) the amount of seconds to wait in between the measurements
"""        
class DigitalTemperatureThread(SiSThread):
    """
    exchange - (DataExchange) the exchange object
    interval - (int) the predefined interval in which the new value of the geiger
                     counter is updated
    devices - (list/string) the list containing the paths to the individual
                            paths to the directories of the single sensors
    """ 
    def __init__(self, dataexchange, interval=2):
        SiSThread.__init__(self, dataexchange)
        self.interval = interval
        # initializing the one wire bus system with the linux commands
        # for the raspberry pi
        os.system("sudo modprobe wire")
        os.system("sudo modprobe w1-gpio")
        os.system("sudo modprobe w1-therm")
        # the list of paths to the files of the individual devices
        self.devices = []
        index = 1
        for device_path in os.listdir("/sys/bus/w1/devices"):
            if device_path.startswith("10") or device_path.startswith("28"):
                self.devices.append("/sys/bus/w1/devices/"+device_path+"/w1_slave")
                self.exchange.register_sensor("temp"+str(index))
                index += 1
                print("lol")
        self.exchange.log("[+] created Temperature Thread")
                
    def run(self):
        """
        the threading main loop in dependency of the exchanged programstate.
        ###
        RETURNS (void)
        """
        self.exchange.log("[+] running Temperature Thread")
        # main loop with the exchanged programstate condition
        # the starting time to time the interval later on
        t_start = time.time()
        try:
            while self.exchange.programstate:
                t_delta = time.time() - t_start
                if t_delta >= self.interval:
                    self._update_data()
                    t_start = time.time()
        finally:
            self.exchange.log("[*] terminated Temperature Thread")
                
    def _read_temperature(self, device):
        """
        attempts to read the temperature of a single device either until a 
        value has been found within the temporary file of the device. If the
        attempt is succesful, returns a float with the value of the meassured
        temperature, otherwise returns a string telling that the attempt failed
        ###
        device - (string) the path of the device, that should be meassured
        ###
        RETURN (float)
        """
        temp_file = open(device, "r")
        first, second = temp_file.readlines()
        temp_file.close()
        if not(first.find("YES") == -1):
            return (int(second.split("=")[1]))*0.001
        else:
            return "error"
        
    def _update_data(self):
        """
        reads the data of every individual Temperature Sensor and writes it 
        into the dictionary of the dataexchange object
        ###
        RETURNS (void)
        """
        index = 1
        for device in self.devices:
            self.exchange.set_data("temp"+str(index), self._read_temperature(device))
            index += 1
"""
the thread managing the Gps tracking of the box, using the JTGps.GpsController
class (for detailed information, look up the JTGps Module)
"""            
class GpsThread(SiSThread):
    """
    gpsc - (GpsController) the class to controll access to the received gps data
    exchange - (DataExchange) the exchange object
    interval - (int) the predefined interval in which the new value of the geiger
                     counter is updated
    """
    def __init__(self, dataexchange, file, interval=15):
        # initializing the super class
        SiSThread.__init__(self, dataexchange)
        self.interval = interval 
        # registering the sensors inside the dataexchnage-dictionary
        self.exchange.register_sensor("latitude")
        self.exchange.register_sensor("longitude")
        self.exchange.register_sensor("altitude")
        self.exchange.register_sensor("speed")
        # setting up and starting the gps controlling thread
        self.gps = jtgps.Gps(file)
        self.gps.start()
        
    def run(self):
        """
        the threading main loop in dependency of the exchanged programstate variable.
        calling the _update_data method after the set interval of time has passed
        ###
        RETURNS (void)        
        """
        # setting up the time variable for the interval calculations
        t_start = time.time()
        # starting the main loop with the exchanged programstate condition
        while self.exchange.programstate:
            t_delta = time.time() - t_start
            if t_delta >= self.interval:
                self._update_data()
                t_start = time.time()
                
    def _update_data(self):
        """
        updating the data of the 4 registered sensors: latidude, longitude,
        speed and climb and therefor writing it into the dictionary of the
        dataexchange object
        ###
        RETURNS (void)
        """
        # using the fix attribute of the GpsController class to acces the 
        # single bits of data received from the gps device
        self.exchange.set_data("latitude", self.gps.latitude)
        self.exchange.set_data("longitude", self.gps.longitude)
        self.exchange.set_data("speed", self.gps.speed)
        self.exchange.set_data("altitude", self.gps.altitude)
        
"""
A Thread mainly used for testing the Threads and their functionality during
their developement period
###
dataexchange - (DataExchange) the exchange object
"""
class TestThread(SiSThread):
    """
    pass
    """
    def __init__(self, dataexchange):
        # initializing the super class
        SiSThread.__init__(self,dataexchange)
        
    def run(self):
        """
        the threading main loop in dependency of th exchanged programstate variable.
        Issueing an input prompt for entering an interactive command, passing the
        command through an emulated switch statement of predefined possible commands
        ###
        RETURNS (void)
        """
        while self.exchange.programstate:
            cmd = raw_input(">>> ")
            if cmd == "end" or cmd == "close":
                self.exchange.programstate = False
            if cmd == "list sensors":
                # prints the processes/ the registered sensors
                print("Running Sensor Threads:\n")
                for process in self.exchange.data.keys():
                    print(process)
            if cmd[0:3] == "get":
                if cmd[4:] in self.exchange.data.keys():
                    print(self.exchange.data[cmd[4:]])
                    
class AerosolThread(SiSThread):
    
    def __init__(self, dataexchange, pin, freq):
        # initializing the super class
        SiSThread.__init__(self,dataexchange)
        gpio.setup("pin")        
        self.gpi = gpio.OutputGpio(pin)
        self.freq = freq
        self.interval = int((1/self.freq)/2)
        
    def run(self):
        t_start = time.time()
        while self.exchange.programstate:
            t_delta = time.time() - t_start
            if t_delta >= self.interval:
                self.gpi.toggle()
                t_start = time.time()

                

                
        
                
    