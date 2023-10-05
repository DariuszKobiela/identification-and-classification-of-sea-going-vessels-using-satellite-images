# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Daro')

