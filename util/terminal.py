__author__ = 'Jonas'
import shutil
import JTShell.util.colors as colors


def get_terminal_width():
    return int(str(shutil.get_terminal_size()).replace("os.terminal_size(","").replace(")","").split(",")[0].split("=")[1])


def get_terminal_height():
    return int(str(shutil.get_terminal_size()).replace("os.terminal_size(","").replace(")","").split(",")[1].split("=")[1])


def helplist(dictionary, max_length=20, color="green"):
    # the dictionary to be converted into the list
    dict = dictionary

    # the actual string of the list
    string = "\n"
    for name in dict.keys():
        temp_string = ""
        # adding the name of the function as bold and colored as one of the rgb colors passed
        if color == "green":
            temp_string += colors.bold(colors.green(" "+name))
        elif color == "red":
            temp_string += colors.bold(colors.red(" "+name))
        elif color == "blue":
            temp_string += colors.bold(colors.blue(" "+name))
        # adding the amount of whitespaces missing until the max character count has been reached
        for i in range(0, max_length - len(name), 1):
            temp_string += " "
        # adding the separation
        temp_string += " - "
        # adding the content of the description to the string
        temp_string += dict[name]
        count = 0
        for character in temp_string:
            string += character
            if count == get_terminal_width() + 15:
                string += "\n" + (" " * (max_length+4))
                count = 0
            if len(str(character)) == 1:
                count += 1
        if string[-1] != "\n":
            string += "\n"
    return string
