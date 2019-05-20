#!/usr/bin/env python3

import sys
import questable
from cprint import RED, GREEN, YELLOW, cprint


def handled_input(prompt):
    try:
        i = input(prompt)
    except EOFError:
        print("")
        sys.exit(0)
    except KeyboardInterrupt:
        print("")
        sys.exit(0)
    return i


def add_quest(side_quest):
    pass


def list_quest(side_quest):
    # If functions called from within list_quests change the state of the
    # database in a way that the list_quests gets outdated, change the state

    state = {"update": False}
    quests = questable.get_quests(side_quest)
    quests.sort(key=lambda i: (i["priority"], -i["id"]), reverse=True)
    while True:
        if state["update"]:
            quests = questable.get_quests(side_quest)
            state["update"] = False
        if quests is False:
            cprint("Invalid Token!", RED)
            sys.exit(1)

        print("")
        cprint("Choose a " + "side " * side_quest + "quest", GREEN)
        print("")
        for q in quests:
            cprint(str(q["id"]) + ". " + q["name"], YELLOW)
        cprint("b. Back", YELLOW)
        print("")
        while True:
            try:
                i = handled_input("> ")
                if i == "b":
                    print("")
                    return
                qid = int(i)
                quest(side_quest, qid, state)
                break
            except(ValueError):
                cprint("Not a quest ID", RED)
                print("")


def status():
    player = questable.player()
    cprint("""
XP: {}
Quests: {}/{}
Side Quests: {}/{}
           """.format(
               player["xp"],
               player["quests_completed"],
               player["total_quests"],
               player["side_quests_completed"],
               player["total_side_quests"]
           ), GREEN)


def quest(side_quest, qid, state):
    q = questable.get_quest(side_quest, qid)
    if "error" in q:
        cprint(q["error"], RED)
        return
    cprint(
        """
ID: {}
Name: {}
Difficulty: {}
Priority: {}
State: {}
        """.format(
            q["id"],
            q["name"],
            [None, "Low", "Medium", "High"][q["difficulty"]],
            [None, "Low", "Medium", "High"][q["priority"]],
            "Completed" if q["state"] else "Incomplete"
        ), GREEN)
    if q["state"] is True:
        cprint("b. Back", YELLOW)
        print("")
        handled_input("> ")
        return

    cprint("1. Mark as done", YELLOW)
    cprint("2. Edit Name", YELLOW)
    cprint("3. Change Priority", YELLOW)
    cprint("4. Change Difficulty", YELLOW)
    cprint("5. Delete Quest", YELLOW)
    cprint("b. Back", YELLOW)
    cprint("", YELLOW)
    i = handled_input("> ")
    if i == "b":
        return
    elif i == "1":
        mark_as_done(side_quest, qid)
        state["update"] = True
    elif i == "2":
        edit_name(side_quest, qid)
        state["update"] = True
    elif i == "3":
        change_priority(side_quest, qid)
    elif i == "4":
        change_difficulty(side_quest, qid)
    elif i == "5":
        delete_quest(side_quest, qid)
        state["update"] = True
    else:
        cprint("Invalid Option", RED)


def mark_as_done(side_quest, qid):
    pass


def edit_name(side_quest, qid):
    pass


def change_priority(side_quest, qid):
    pass


def change_difficulty(side_quest, qid):
    pass


def delete_quest(side_quest, qid):
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
    cprint("Choose an option", GREEN)
    print("")
    cprint("1. Add a quest", YELLOW)
    cprint("2. Add a side quest", YELLOW)
    cprint("3. List quests", YELLOW)
    cprint("4. List side quests", YELLOW)
    cprint("5. Check status", YELLOW)
    cprint("q. Quit", YELLOW)
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
