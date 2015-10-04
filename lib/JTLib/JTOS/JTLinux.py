# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 16:56:05 2015
@author: Jonas
###
descripton
"""
import os

def createfile(path):
    """
    creates a file
    ###
    path - (string) the path of the file to be created
    """
    if not(os.path.exists(path)):
        try:
            os.system("touch "+path)
        except:
            print("couldnt create file: "+path)