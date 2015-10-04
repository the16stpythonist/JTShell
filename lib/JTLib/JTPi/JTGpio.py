# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 08:31:44 2015
@author: Teufel.Jonas
###
placeholder
"""
import time as t
import RPi.GPIO as GPIO
import re

def setup(mode):
    """
    setting up the possibility to use the gpio library also determining the way,
    that the RaspberryPi is indexing its pins. Therefor either uses the default
    pin indexing or the plain gpio numbering 
    ###
    mode - (string) either "gpio" or "pin". determining which mode to be used
    ###
    RETURNS (void)
    """
    # checking for parameter type
    if type(mode) is str:
        if mode == "gpoi" or mode == "Gpio":
            GPIO.setmode(GPIO.BCM)
        elif mode == "pin" or mode == "Pin":
            GPIO.setmode(GPIO.BOARD)
            
def cleanup():
    """
    simply calls the cleanup command to remove all configurations to prevent
    further errors withing the RaspberryPi's accesing functionalities. Doing nothing
    else but opening the software-sided boundries of the ports. Has to be called at
    the end of every program cycle.
    ###
    RETURNS (void)
    """
    GPIO.cleanup()
            
    
"""
a class managing a single GPIO port on the RaspberryPi. works as an interface
###
port - (int) depending on the model and the previously defined layout mode
             an interger-index from 1 to about 26
"""
class Gpio():
    """
    port - (int) depending on the model and the previously defined layout mode
                 an interger-index from 1 to about 26
    mode - (string) if the defined mode of an Gpio object isnt clear this will
                    will check wether the gpio is set to Input or to output mode
    """
    def __init__(self,port, mode):
        self.port = 0
        self.mode = mode
        if type(port) is int:
            if port in range(1,22,1):
                self.port = port
                
    
"""
a class to represent a RaspberryPi on input mode. providing the functionality to
check wether the port is high or low and also being able to define an internal 
pull-up or pull down resistor
###
port - (int) depending on the model and the previously defined layout mode
             an interger-index from 1 to about 26.
pull - (string) either "up", "down" or None/False. Symbolzing which internal
                pull resistor should be used upon initialization.
"""
class InputGpio(Gpio):
    """
    port - (int) depending on the model and the previously defined layout mode
                 an interger-index from 1 to about 26
    mode - (string) if the defined mode of an Gpio object isnt clear this will
                    will check wether the gpio is set to Input or to output mode
    """
    def __init__(self, port, pull=None):
        Gpio.__init__(self, port, "INPUT")
        if type(pull) is str:
            if re.match(r"[Dd][Oo][Ww][Nn]", pull):
                GPIO.setup(self.port, GPIO.IN, pull_up_down=GPIO.BUD_DOWN)
            elif re.match(r"[Uu][Pp]", pull):
                GPIO.setup(self.port, GPIO.IN, pull_up_down=GPIO.BUD_UP)
        else:
            GPIO.setup(self.port, GPIO.IN)
        
    def get_state(self):
        """
        reads the input at the given Gpio
        ###
        RETURNS (boolean)
        """
        if GPIO.input(self.port) == GPIO.HIGH:
            return True
        else:
            return False

"""
a class to represent a RaspberryPi on input mode. providing the functionality to
check wether the port is high or low and also being able to define an internal 
pull-up or pull down resistor
###
port - (int) depending on the model and the previously defined layout mode
             an interger-index from 1 to about 26.

"""
class OutputGpio(Gpio):
    """
    port - (int) depending on the model and the previously defined layout mode
                 an interger-index from 1 to about 26
    mode - (string) if the defined mode of an Gpio object isnt clear this will
                    will check wether the gpio is set to Input or to output mode
    state -(bool) the current state of the pin, wether its High or Low
    """
    def __init__(self, port, pull=None):
        Gpio.__init__(self, port, "OUTPUT")
        if type(pull) is str:
            if re.match(r"[Dd][Oo][Ww][Nn]", pull):
                GPIO.setup(self.port, GPIO.OUT, pull_up_down=GPIO.BUD_DOWN)
            elif re.match(r"[Uu][Pp]", pull):
                GPIO.setup(self.port, GPIO.OUT, pull_up_down=GPIO.BUD_UP)
        else:
            GPIO.setup(self.port, GPIO.OUT)
        GPIO.output(self.port, False)
        self.state = False
        
    def change_state(self, boolean):
        """
        depending on the current state of the pin, this changes the state to
        the state given by parameter if possible or in case it is already the 
        given state itll be left like it was.
        ###
        boolean - (bool)   the boolean state of 1 and 0 (True and False)
                  (string) the string state of 1 and 0
        ###
        RETURNS (void)
        """
        if type(boolean) is bool:
            # actually changing the state
            if self.state != boolean:
                self.state = boolean
                GPIO.output(self.port, self.state)
                
        elif type(boolean) is str:
            # actually changing the state
            val = True
            if boolean == "1":
                val = True
            elif boolean == "0":
                val = False
            if self.state != val:
                self.state = val
                GPIO.output(self.port, self.state)
                
        elif type(boolean) is int:
            # actually changing the state
            val = True
            if boolean == 1:
                val = True
            elif boolean == 0:
                val = False
            if self.state != val:
                self.state = val
                GPIO.output(self.port, self.state)

    def pull(self, state, time):
        """
        depending on the current state of the pin this method will either pull
        the voltage of the pin up or down for the given amount of time in seconds.
        returns a boolean value for wether the state of the pin was able to
        perform a pull or not.
        ###
        state - (string) either 'up' or 'down' for 3v3 or Gnd
                (bool) either True of False for 3v3 or Gnd
                (int) either 1 or 0 for 3v3 or Gnd
        time - (float) the time to pull the wire in seconds
        ###
        RETURNS (bool)
        """
        # in case its an pull up
        if state==1 or state=="up" or state==True or state=="UP":
            if self.state == False:
                self.change_state(True)
                t.sleep(time)
                self.change_state(False)
                return True
            else:
                return False
        # in case its a pull down
        elif state==0 or state=="down" or state==False or state=="DOWN":
            if self.state == True:
                self.change_state(False)
                t.sleep(time)
                self.change_state(True)
                return True
            else:
                return False
            
    def toggle(self):
        """
        depending on what state the outputpin is set this method toggles the
        state, meaning inverting it
        ###
        RETURNS (void)
        """
        if self.state == True:
            self.change_state(False)
        else:
            self.change_state(True)
                        
      