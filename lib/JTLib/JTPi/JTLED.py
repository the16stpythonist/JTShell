# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 20:20:14 2015

@author: Jonas
"""
import JTLib.JTPi.JTGpio as io
import time
import random
import sys

"""
An abstract base class representing a Matrix
###
gpiolist      -  (list/int) a list with all gpio ports as integers
                 (list/str) a list with all gpio ports as strings
"""
class LED_Matrix():
    """
    gpiolist - (list/int) a list with all gpio ports as integers
               (list/str) a list with all gpio ports as strings
    matrixdictionary - (dict(tuple-JTGpio.Gpio)) a dictionary giving every 2-dimensional
                                                 integer index tuple a Gpio object
                                                 to manage
    totalamount - (int) the length of the gpiolist, representing the total
                        amount of LEDs used in the matrix
    """
    def __init__(self, gpiolist):
        self.gpiolist = []
        if type(gpiolist) is list:
            self.gpiolist = gpiolist
            if type(gpiolist[0]) is str:
                self._calcintgpiolist()
        self.totalamount = len(self.gpiolist)
        self.matrixdictionary = {}
          
    def _calcintgpiolist(self):
        """
        Converting a self.gpiolist with string items into a self.gpiolist with 
        integer items
        ###        
        RETURNS (void)
        """ 
        temp_list = []
        for substring in self.gpiolist:
            temp_list.append(int(substring))
        self.gpiolist = temp_list
        
    def get_gpiolist(self):
        """
        returns a list with all the used gpio port indexes within the curent matrix
        ###
        RETURNS (list/int)
        """
        return self.gpiolist
        
    def get_totalamount(self):
        """
        returns the total amount of used LEDs within the matrix
        ###
        RETURNS (int)
        """
        return self.totalamount
        

"""
An abstract base class representing a Matrix
###
gpiolist - (list/int) a list with all gpio ports as integers
           (list/str) a list with all gpio ports as strings
rows - (int) the amount of rows on the matrix
columns - (int) the amount of columns on the matrix
"""        
class LED_2DMatrix(LED_Matrix):
    """
    VARIABLES
    gpiolist - (list/int) a list with all gpio ports as integers
               (list/str) a list with all gpio ports as strings
    matrixdictionary - (dict(tuple/JTGpio.Gpio)) a dictionary giving every 2-dimensional
                                                 integer index tuple a Gpio object
                                                 to manage
    totalamount - (int) the length of the gpiolist, representing the total
                        amount of LEDs used in the matrix
    row_count - (int) the amount of rows on the matrix
    column_count - (int) the amount of columns on the matrix
    """
    def __init__(self, gpiolist, columns, rows):
        LED_Matrix.__init__(self, gpiolist)
        self.row_count = rows
        self.column_count = columns
        gpio_index = 0
        if type(gpiolist) is list:
            if (self.row_count * self.column_count) >= self.totalamount:
                for a in range(0, self.row_count, 1):
                    for b in range(0, self.column_count, 1):
                        self.matrixdictionary[(a,b)] = io.OutputGpio(self.gpiolist[gpio_index])
        elif type(gpiolist) is dict:
            for key, value in gpiolist.iteritems():
                self.matrixdictionary[key] = io.OutputGpio(value)
        
    def on(self, x, y):
        """
        turns on the specified LED
        ###
        index_tuple  -  (tuple/int-int) a tuple with the 2dimensional coordinates 
                                        of the LED
        ###
        RETURNS (void)
        """
        self.matrixdictionary[(x,y)].change_state(True)
        
    def off(self, x, y):
        """
        turns off the specified LED
        ###
        index_tuple  -  (tuple/int-int) a tuple with the 2dimensional coordinates 
                                        of the LED
        ###
        RETURNS (void)
        """
        self.matrixdictionary[(x,y)].change_state(False)
        
    def delay(self, t):
        """
        calls the sleep function
        ###
        t - (int) the amount of time to delay in seconds
        ###
        RETURNS (void)
        """
        time.sleep(t)


"""
An abstract base class representing a Matrix
###
gpiolist - (list/int) a list with all gpio ports as integers
           (list/str) a list with all gpio ports as strings
"""
class LED_2DMatrix_4x5y(LED_2DMatrix):
    """
    gpiolist      -  (list/int) a list with all gpio ports as integers
                     (list/str) a list with all gpio ports as strings
    matrixdictionary
                  -  (dict(tuple/JTGpio.Gpio)) a dictionary giving every 2-dimensional
                                               integer index tuple a Gpio object
                                               to manage
    totalamount   -  (int) the length of the gpiolist, representing the total
                           amount of LEDs used in the matrix
    row_count     -  (int) the amount of rows on the matrix
    column_count  -  (int) the amount of columns on the matrix
    """
    def __init__(self, gpiolist):
        LED_2DMatrix.__init__(self, gpiolist, 4, 5)
        
    def raindrops(self, loops, speed):
        """
        the raindrop animation.
        only one raindrop at a time
        ###
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 0.1 * (speed / 100)
        # the amount of repetitions        
        for n in range(0, loops, 1):
            columns = [0, 1, 2, 3]
            # first drop
            column = columns.pop(random.randint(1,len(columns)-1))
            for a in range(0,5,1):
                self.on(column, 4-a)
                self.delay(t)
                self.off(column, 4-a)
            # first drop
            column = columns.pop(random.randint(1,len(columns)-1))
            for a in range(0,5,1):
                self.on(column, 4-a)
                self.delay(t)
                self.off(column, 4-a)
            # first drop
            column = columns.pop(random.randint(1,len(columns)-1))
            for a in range(0,5,1):
                self.on(column, 4-a)
                self.delay(t)
                self.off(column, 4-a)
            # first drop
            column = columns[0]
            for a in range(0,5,1):
                self.on(column, 4-a)
                self.delay(t)
                self.off(column, 4-a)
                
    def inverting_chess(self, loops, speed):
        """
        a chess style layout of turned on LEDs which is inverting after a short pause
        ###        
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###        
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 4 * (speed / 100)
        # the amount of repetitions        
        for n in range(0, loops, 1):
            # mode 
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(0, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(1, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(2, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(3, 4-a)
            self.delay(t)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.off(0, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.off(1, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.off(2, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.off(3, 4-a)
            # inverted mode
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(0, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(1, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(2, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(3, 4-a)
            self.delay(t)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(0, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(1, 4-a)
            for a in range(0,5,1):
                if a in [2,4]:
                    self.on(2, 4-a)
            for a in range(0,5,1):
                if a in [1,3,5]:
                    self.on(3, 4-a)
                    
    def vertical_lines(self, loops, speed):
        """
        makes a vertical line that goeas right and than back left
        ###        
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###        
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 2 * (speed / 100)
        # the amount of repetitions        
        for n in range(0, loops, 1):
            for x in [0, 1, 2, 3, 2, 1, 0]:
                for y in [0,1,2,3,4]:
                    self.on(x,y)
                self.delay(t)
                for y in [0,1,2,3,4]:
                    self.off(x,y)
                    
    def horizontal_lines(self, loops, speed):
        """
        makes a horizontal line that goes down and up and back down
        ###        
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###        
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 2 * (speed / 100)
        # the amount of repetitions        
        for n in range(0, loops, 1):
            for y in [0, 1, 2, 3, 4, 3, 2, 1, 0]:
                for x in [0,1,2,3]:
                    self.on(x,y)
                self.delay(t)
                for x in [0,1,2,3]:
                    self.off(x,y)
                
    def rings(self, loops, speed):
        """
        creates an inner and outer ring 
        ###        
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###        
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 2 * (speed / 100)
        # the amount of repetitions        
        for n in range(0, loops, 1):
            # outer ring on
            for y in [0, 1, 2, 3, 4]:
                self.on(0,y)
                self.on(3,y)
            self.on(1,0)
            self.on(2,0)
            self.on(1,4)
            self.on(2,4)
            self.delay(t)
            for y in [0, 1, 2, 3, 4]:
                self.off(0,y)
                self.off(3,y)
            self.off(1,0)
            self.off(2,0)
            self.off(1,4)
            self.off(2,4)
            # inner ring on
            self.on(1, 1)
            self.on(1, 2)
            self.on(1, 3)
            self.on(2, 1)
            self.on(2, 2)
            self.on(2, 3)
            self.delay(t)
            self.off(1, 1)
            self.off(1, 2)
            self.off(1, 3)
            self.off(2, 1)
            self.off(2, 2)
            self.off(2, 3)
            
    def all_on(self, loops, speed):
        """
        turns all LEDS on
        ###
        loops   -  (int) the amount of loops
        speed   -  (int) the speed of the animation in percent
        ###
        RETURNS (void)
        """
        # the pause between animations, dependant on the speed
        t = 2 * (speed / 100)
        # the amount of repetitions        
        for y in [0,1,2,3,4]:
            for x in [0,1,2,3]:
                self.on(x,y)
        self.delay(t)
        for y in [0,1,2,3,4]:
            for x in [0,1,2,3]:
                self.off(x,y)
            
"""
Die LED matrix für das Informatik projekt
###
gpiolist - (list/int) a list with all gpio ports as integers
           (list/str) a list with all gpio ports as strings
"""
class Inf_window_Matrix(LED_2DMatrix_4x5y):
    """
    gpiolist - (list/int) a list with all gpio ports as integers
                     (list/str) a list with all gpio ports as strings
    matrixdictionary - (dict(tuple/JTGpio.Gpio)) a dictionary giving every 2-dimensional
                                                 integer index tuple a Gpio object
                                                 to manage
    totalamount - (int) the length of the gpiolist, representing the total
                        amount of LEDs used in the matrix
    row_count - (int) the amount of rows on the matrix
    column_count - (int) the amount of columns on the matrix
    """
    def __init__(self, gpiolist):
        LED_2DMatrix_4x5y.__init__(self, gpiolist)   

    def run(self):
        """
        actually starting the animations
        ###
        RETURNS (void)
        """
        # the amount of repetitions 
        try:
            while (True):
                self.raindrops(20, 100)
                self.pause()
                self.vertical_lines(3, 150)
                self.pause()
                self.horizontal_lines(3, 150)
                self.pause()
                self.inverting_chess(8, 100)
                self.pause()
                self.rings(8, 100)
                self.pause()
        except:
            io.cleanup()
            sys.exit()    
            
    def pause(self):
        self.delay(3)
        self.all_on(3, 100)
        self.delay(3)