#!/usr/bin/env python3

import sys
import questable
from cprint import RED, GREEN, cprint


def handled_input(prompt):
    try:
        i = input(prompt)
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
    return i


def add_quest(side_quest):
    pass


def list_quest(side_quest):
    pass


def status():
    pass


cprint("Welcome to questable.", GREEN)
print("")
cprint("Trying to authenticate token . . . ", GREEN)
if questable.auth():
    cprint("Authentication successful", GREEN)
    print("")
else:
    cprint("Authentication failed! Please check your Token / API URL", RED)
    sys.exit(1)


while True:
    print("Choose an option")
    print("1. Add a quest")
    print("2. Add a side quest")
    print("3. List quests")
    print("4. List side quests")
    print("5. Check status")
    print("q. Quit")
    print("")
    while True:
        i = handled_input("> ")
        if i == "q":
            sys.exit(0)
        try:
            i = int(i)
            if not 0 < i <= 5:
                raise ValueError
            break
        except ValueError:
            cprint("Invalid Option", RED)
            print("")
    if i == 1:
        add_quest(False)
    elif i == 2:
        add_quest(True)
    elif i == 3:
        list_quest(False)
    elif i == 4:
        list_quest(True)
    elif i == 5:
        status()
