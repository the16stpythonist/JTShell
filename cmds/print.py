__author__ = 'Jonas'
import os, shutil
import JTShell.util.colors as c

help = {"desc":"a function used to print the entered string, mainly used for testing",
        "std":"the string to be printed"}


def run(process, std="nothing"):
    print(c.bold("a"))
    print(c.bold(c.green("a")))
    print(c.green("a"))
    print(c.bold(c.red("a")))
    print(c.red("a"))
    print(c.bold(c.blue("a")))
    print(c.blue("a"))
    print(c.bold(c.yellow("a")))
    print(c.yellow("a"))
    return "a"