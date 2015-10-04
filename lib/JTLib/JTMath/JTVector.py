# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:32:42 2015
@author: Jonas
"""
import math as math
import numpy.linalg as linalg

# FUNCTIONS
def same_dimension(*args):
    """
    returns wether all passed arguments/objects are "DimensionalObjects" and
    wether they are all represented in the same dimensions
    ###
    args* - (DimensionalObject) the objects to be compared with one another
    ###
    RETURNS (bool)
    """
    # checking wether every object implements the DimensionalObject Interface
    for argument in args:
        if not(isinstance(argument, DimensionalObject)):
            return False
    # in case all abjects are DimensionalObjetcs, comparing the result of the
    # implemented "get_dimensions" method
    ref_value = args[0].get_dimensions()
    for argument in args:
        if not(argument.get_dimensions() == ref_value):
            return False
    # in case no False has already been returned, returns True
    return True
    
    
            

# CLASSES
"""
the Error to b raised whenever, the program wants to process two objects of
different dimensions
###
message - (string) the standard message/output of the Error
"""
class DimensionalError(Exception):
    def __init__(self, *objects):
        # putting together the standard message with the string representations
        # of the passed Objects
        message = ""
        # checking if the objects are "DimensionalObjects"
        if objects:
            message += "Error raised by processing the following DimensionalObjects\n"            
            for obj in objects:
                if isinstance(obj, DimensionalObject):
                    message += str(obj)                    
        # calling the constructor of the base class Exception
        super(DimensionalError, self).__init__(message)
        



"""
An Interface for every object with dimensions, that can be projected 
onto a kartheisian coordinate system, implements the "get_dimensions" 
function into the object, that returns an integer with the number of
dimensions in which the object is present.
"""
class DimensionalObject():
    
    def __init__(self):
        pass

    def get_dimensions(self):
        pass        

    def __str__(self):
        pass        

"""
Defines a point in an n-dimensional space 
"""
class Point(DimensionalObject):
    """
    coordinates - (list/int) the list containing the coordinates of the point
                             relative to the origin 
    """
    def __init__(self, *args,**kwargs):
        DimensionalObject.__init__(self)
        # the coordinates list of the point
        self.coordinates = []
        
        if args:
            
            # getting the coordinates in case the args list consists of only int
            only_integers = True
            for argument in args:
                if type(argument) is not int:
                    only_integers = False
            if only_integers:
                # assigning the integers to the "self.coordinates" list
                self.coordinates = args
                
            # getting the coordinates in case there is only one list given
            if len(args) == 1 and type(args[0]) is list:
                self.coordinates = args[0]
                
            # getting the coordinates in case there is only one tuple given
            if len(args) == 1 and type(args[0]) is tuple:
                self.coordinates = list(args[0])
                    
    def get_dimensions(self):
        """
        returns the amount of dimensions in which the object is projected
        ###
        RETURNS (int)
        """
        return len(self.coordinates)
        
    def __eq__(self, other):
        """
        defines the behaviour for the "==" Operator used on the object, in 
        case the compared object is another Point-object it returns true if
        the coordinates of the two points are equal and false in case they are
        not.
        ###
        other - (Point) the Point object to wich the current object is
                        compared to
        ###
        RETURNS (bool)
        """
        # if the "other" object is also a Point
        if type(other) is Point:
            if self.coordinates == other.coordinates:
                return True
            else:
                return False
        
    def __ne__(self, other):
        """
        defines the behaviour for the "!=" Operator used on the object, in
        case the compared object is another Point-object it returns false if
        the coordinates of the two points are equal and true in case they are
        not.
        ###
        other - (Point) the Point object to which the current object is
                        compared to
        ###
        RETURNS (bool)
        """
        # if the "other" object is also a Point
        if type(other) is Point:
            if self.coordinates == other.coordinates:
                return False
            else:
                return True
                
    
    def value(self, dimension):
        """
        returnes the value of the given dimension parameter, meaning the integer
        value of the coordinates list at the given index
        ###
        dimension - (int) the index of the dimension
        ###
        RETURNS (int)
        """
        return self.coordinates[dimension]
        
    def move(self, arg):
        """
        moves the point object, meaning changing the coordinates
        ###
        args* - (list/int) a list with the new coordinates of the point 
                (Point) moves the Point to the location of the passed point
                (Vector) moves the point into through the vector
        ###
        RETURNS (void)
        """
        # in case only integers are passed to the method             
        if type(arg) is list and len(arg) == self.get_dimensions():
            self.coordinates = arg
        # in case a point has been passed
        elif isinstance(arg, Point) and same_dimension(arg, self):
            self.coordinates = arg.coordinates
        # in case a vector has been passed
        elif isinstance(arg, Vector) and same_dimension(arg, self):
            self.coordinates += arg.coordinates
        else:
            raise DimensionalError(self, arg)
           
    def __str__(self):
        """
        implements behviour for whenever the object is issued with a string
        conversion, mostly through the function "str()"
        ###
        RETURNS (string)
        """
        result = "P("
        for coordinate in self.coordinates:
            result += str(coordinate) + "/"
        return result[:-1] + ")"
         
"""
Defines a vector in a n-dimensional space, that can be defined by passing the 
coordinates relativ to the origin to the constructor, which will then be 
interpreted as a base vector, this can be acomplished by passing integers, a 
list or tuple containing integers or a point object. The Vector can also be 
defined by passing two point objects to the constructor, the resulting vector
will be the one between those points.
"""
class Vector(DimensionalObject):
    """
    coordinates - (list/int) the list containing the dimensional parts of the
                             vector
    length - (int) the length of the vector
    """
    def __init__(self, *args, **kwargs):
        DimensionalObject.__init__(self)
        # the coordinates list of the point 
        self.coordinates = []
        self.length = 0
        
        if args and not(kwargs):
            
            # getting the coordinates in case the args list consists of only int
            only_integers = True
            for argument in args:
                if type(argument) is not int:
                    only_integers = False
            if only_integers:
                # assigning the integers to the "self.coordinates" list
                self.coordinates = args
                
            # getting the coordinates in case there is only one list given
            elif len(args) == 1 and type(args[0]) is list:
                self.coordinates = args[0]
                
            # getting the coordinates in case there is only one tuple given
            elif len(args) == 1 and type(args[0]) is tuple:
                self.coordinates = list(args[0])
                
            # getting the coordinates in case there is only one Point-object
            elif len(args) == 1 and type(args[0]) is Point:
                self.coordinates = args[0].coordinates
                
            # getting the coordinates in case there is only two Point objects
            # and the vector is two be drwan in between them
            elif len(args) == 2 and type(args[0]) is Point and type(args[1]) is Point:
                # substracting the coordinates in case they are both in the
                # same dimension
                if args[0].get_dimensions() == args[1].get_dimensions():
                    self.coordinates = []
                    for n in range(0,len(args[0].coordinates)):
                        self.coordinates.append(args[1].coordinates[n] - args[0].coordinates[n])
                    
            # getting the coordinates in case there is only a Vector object
            elif len(args) == 1 and type(args[0]) == Vector:
                self.coordinates = args[0].coordinates
                
        elif kwargs:
            
            # getting the coordinates with a list of integers 
            if ("coordinates" in kwargs.keys()) and type(kwargs["coordinates"]) is list:
                self.coordinates = kwargs["coordinates"]
            
            # getting the coordinates from a Point object given
            if ("point" in kwargs.keys()) and type(kwargs["point"]) is Point:
                self.coordinates = kwargs["point"].coordinates
            
            # getting the coordinates from two Point objects given
            if ("points" in kwargs.keys()) and type(kwargs["points"]) is tuple:
                self.coordinates = kwargs["points"][1].coordinates - kwargs["points"][0].coordinates
        
        # calculates the length of the vector
        self._calc_length()                
        
    def _calc_length(self):
        """
        calculates the length of the vector via the pythagoras
        ###
        RETURNS (void)
        """
        # calculates the sum of the squares of the dimension-parts
        quad_sum = 0
        for dimension in self.coordinates:
            quad_sum += dimension**2
        # assignes the length as the square root of the quadratic sum
        self.length = math.sqrt(quad_sum)
        
    def __len__(self):
        """
        returns the length of the vector upon calling the built in len() function
        on an Vector-object
        ###
        RETURNS (int)
        """
        return self.length
        
    def __add__(self, other):
        """
        implements behaviour whenever the addition operator is used on the
        object and another vector object, simply adds every matching
        dimensional value.
        ###
        other - (Vector) the vector to be added
        ###
        RETURNS (Vector)
        """
        if type(other) is Vector and same_dimension(self, other):
            return Vector(self.coordinates + other.coordinates)
        else:
            raise DimensionalError(self, other)            
            
    def __sub__(self, other):
        """
        implements behaviour whenever the substraction operator is used on the
        object and another vector object, simply substracts every matching
        dimensional value.
        ###
        other - (Vector) the vector to be substracted
        ###
        RETURNS (Vector)
        """
        if type(other) is Vector and same_dimension(self, other):
            return Vector(self.coordinates - other.coordinates)
        else:
            raise DimensionalError(self, other)
    
    def __mul__(self, other):
        """
        implements behaviour for the multiplication operator for the two cases
        - the other object is another Vector, then itll perform a skalar
          multiplication on the two Vectors and returns the integer result
        - the other ibject is an integer, then itll multiply the integer, with 
          every dimension of the object and rerturns the resulting Vector
        ###
        other - (Vector) the Vector to be multiplied with
                (int) the integer, with wich every dimensional part is to
                      to be multiplied
        ###
        RETURNS (int)
        """
        # the case of "other" being another vector to perform skalar multiplication on
        if type(other) is Vector and same_dimension(self, other):
            result = 0
            # performs Skalar-multiplikation, maining multiplying the same 
            # dimensional part and adding together the resulting products
            for dimension in range(len(self.coordinates)):
                result += self.coordinates[dimension] * other.coordinates[dimension]
            return result
        # the case of "other" being an integer
        elif type(other) is int:
            # creatin a new list to append every multiplied dimension of the
            # Vector to and then ultimatly use to return a new Vector object
            # based on the list created
            coords = []
            for coordinate in self.coordinates:
                coords.append(coordinate*other)
            return Vector(coords)
        else:
            raise DimensionalError(self, other)
            
    def __str__(self):
        """
        implements behviour for whenever the object is issued with a string
        conversion, mostly through the function "str()"
        ###
        RETURNS (string)
        """
        result = "V("
        for coordinate in self.coordinates:
            result += str(coordinate) + "/"
        return result[:-1] + ")"
            
    def is_orthogonal(self, other):
        """
        checks wether a passed Vector object is orthogonal to this one, by
        checking wether the Skalarproduct is zero or not
        ###
        other - (Vector) the Vector to check with
        ###
        RETURNS (bool)
        """
        if type(other) is Vector and same_dimension(self, other):
            # calculates the skalarproduct with the multiply operator            
            if self * other == 0:
                return True
            else:
                return False
        else:
            raise DimensionalError(self, other)
            
    def is_paralell(self, other):
        """
        checks wether a passed Vector object is paralell to the self Vector, by
        checking wether the dimensional components of the vectors have a linear
        dependency on each other
        ###
        other - (Vector) the Vector to check with
        ###
        RETURNS (bool)
        """
        if type(other) is Vector and same_dimension(self, other):
            # calculates the first quotient of the two first dimensional components
            # then checks wether the other quotients are the same
            initial_quotient = self.coordinates[0] / other.coordinates[0]
            for i in range(1,self.get_dimensions()-1):
                temp_quotient = self.coordinates[i] / other.coordinates[i]
                if not(temp_quotient == initial_quotient):
                    return False
            # in case false hasnt already been returned, assuming they are paralell
            return True
        else:
            raise DimensionalError(self, other)
            
    def get_dimensions(self):
        """
        returns the amount of dimensions in which the object is projected
        ###
        RETURNS (int)
        """
        return len(self.coordinates)
        
        
"""
a class representing a line object in an n-dimensional space, that can be
defined by the following ways:
- passing the constructor exactly two point objects, through wich the line
  schould go
- passing the constructor two vector, from wich the first will be used as the
  support vector and the second one will be representing the direction vector
###
*support - (Vector, Point) the support vector of the line
*direction - (Vector) the direction vector of the line
"""
class line(DimensionalObject):
    """
    direction_vector - (Vector) the direction Vector defining the line
    support_vectot - (Vector) the support VEctor defining the line
    """
    def __init__(self,*args,**kwargs):
        DimensionalObject.__init__(self)
        # the two vectors defining the line
        self.direction_vector = None
        self.support_vector = None
        
        if args and not(kwargs):
            
            # in case two Point objects have been passed
            if (len(args)==2 and type(args[0]) is Point and type(args[1]) is Point):
                # creating one Vector through the source(0,0,0...) and the first
                # point and the seconde Vector through the two given Points
                self.support_vector = Vector(Point(0,0,0), args[0])
                self.direction_vector = Vector(args[0],args[1])
            
            # in case two vectors have been passed
            if (len(args)==2 and type(args[0]) is Vector and type(args[1]) is Vector):
                # just using the both vectors in the order they were passed
                self.support_vector = args[0]
                self.direction_vector = args[1]
                
        elif kwargs:
            if (("support" in kwargs.keys() and "direction" in kwargs.keys()) and
                (type(kwargs["support"]) is Vector and type(kwargs["direction"]) is Vector)):
                self.support_vector = kwargs["support"]
                self.direction_vector = kwargs["direction"]
        
    def __str__(self):
        """
        when the str() operator is called on the line object it will return the
        line in  parameter form by just returning the combination of the strings
        of the two Vector objects
        ###
        RETURNS (string)
        """
        return str(self.support_vector) + " + t" + str(self.direction_vector)
        
    def get_dimensions(self):
        """
        returns the amount of dimensions in which the object is projected
        ###
        RETURNS (int)
        """
        return self.support_vector.get_dimensions()
        
    def __contains__(self, obj):
        """
        implements the behaviour for the "in" opertor for the cases:
        - a Point object is passed
        ###
        obj - (Point) the point to be checked, wether it is on the line or not
        ###
        RETURNS (bool)
        """
        if type(obj) is Point and same_dimension(self, obj):
            pass
        else:
            raise DimensionalError(self, obj)