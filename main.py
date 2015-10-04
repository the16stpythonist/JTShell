from JTShell.shell import Shell
import colorama

if __name__ == '__main__':
    # initializing the colorama module, so that the ansi escape sequence colors can actually be utilized in the shell
    colorama.init()
    # creating the shell object and executing the program loop
    shell = Shell("cmds")
    shell.run()