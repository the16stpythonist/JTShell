# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 10:33:48 2015
@author: Jonas
###
description
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
            os.system("@echo off")
            os.system('''copy nul '''+'''"'''+path+'''"''')
        except:
            print("[!] failed to create path: "+path)
            

    
        
