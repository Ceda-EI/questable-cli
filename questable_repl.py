#!/usr/bin/env python3

import os
import sys
import questable
import argparse
from cprint import RED, GREEN, YELLOW, cprint


def handled_input(prompt):
    while True:
        try:
            i = input(prompt)
        except EOFError:
            print()
            sys.exit(0)
        except KeyboardInterrupt:
            print()
            continue
        return i


def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


def add_quest(side_quest):
    cprint("Enter name of " + "side " * side_quest + "quest", GREEN)
    print()
    name = handled_input("> ")
    clear()
    cprint("Choose priority", GREEN)
    print()
    cprint("1. Low", YELLOW)
    cprint("2. Medium", YELLOW)
    cprint("3. High", YELLOW)
    print()
    while True:
        try:
            priority = int(handled_input("> "))
            if priority not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            cprint("Invalid Value", RED)
    clear()
    cprint("Choose difficulty", GREEN)
    print()
    cprint("1. Low", YELLOW)
    cprint("2. Medium", YELLOW)
    cprint("3. High", YELLOW)
    print()
    while True:
        try:
            difficulty = int(handled_input("> "))
            if difficulty not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            cprint("Invalid Value", RED)
    clear()
    q = questable.add_quest(side_quest, name, priority, difficulty)
    if 'error' in q:
        cprint("Failed adding " + "side " * side_quest + "quest", RED)
        cprint(q["error"], RED)
    else:
        cprint("Added " + "side " * side_quest + "quest", GREEN)
        cprint("Side " * side_quest + "Quest ID: " + str(q["id"]), GREEN)
    print()


def list_quest(side_quest):
    # If functions called from within list_quests change the state of the
    # database in a way that the list_quests gets outdated, change the state

    state = {"update": False}
    quests = questable.get_quests(side_quest)
    quests.sort(key=lambda i: (i["priority"], -i["id"]), reverse=True)
    while True:
        if state["update"]:
            quests = questable.get_quests(side_quest)
            quests.sort(key=lambda i: (i["priority"], -i["id"]), reverse=True)
            state["update"] = False
        if quests is False:
            cprint("Invalid Token!", RED)
            sys.exit(1)

        cprint("Choose a " + "side " * side_quest + "quest", GREEN)
        print()
        for q in quests:
            cprint(str(q["id"]) + ". " + q["name"], YELLOW)
        cprint("b. Back", YELLOW)
        print()
        while True:
            try:
                i = handled_input("> ")
                if i == "b":
                    clear()
                    return
                qid = int(i)
                clear()
                quest(side_quest, qid, state)
                break
            except(ValueError):
                cprint("Not a quest ID", RED)
                print()
    clear()


def status():
    player = questable.player()
    cprint(
        """XP: {}
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
        """ID: {}
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
        print()
        handled_input("> ")
        clear()
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
        clear()
        return
    elif i == "1":
        clear()
        mark_as_done(side_quest, qid)
        state["update"] = True
    elif i == "2":
        clear()
        edit_name(side_quest, qid)
        state["update"] = True
    elif i == "3":
        clear()
        change_priority(side_quest, qid)
    elif i == "4":
        clear()
        change_difficulty(side_quest, qid)
    elif i == "5":
        clear()
        delete_quest(side_quest, qid)
        state["update"] = True
    else:
        cprint("Invalid Option", RED)


def mark_as_done(side_quest, qid):
    upd = questable.update_quest(side_quest, qid, state=True)
    if "error" in upd:
        cprint("Error marking " + "side "*side_quest + "quest as done!", RED)
        cprint(upd["error"], RED)
    else:
        xp = ((0 if side_quest else 55) + 10*upd["priority"] +
              15*upd["difficulty"])
        cprint("Marked " + "side "*side_quest + "quest as done!", GREEN)
        cprint("Gained " + str(xp) + " XP", GREEN)


def edit_name(side_quest, qid):
    cprint("Enter new name of " + "side " * side_quest + "quest", GREEN)
    print()
    name = handled_input("> ")
    clear()
    upd = questable.update_quest(side_quest, qid, name=name)
    if "error" in upd:
        cprint("Error changing name", RED)
        cprint(upd["error"], RED)
    else:
        cprint("Changed name ", GREEN)


def change_priority(side_quest, qid):
    cprint("Choose priority", GREEN)
    print()
    cprint("1. Low", YELLOW)
    cprint("2. Medium", YELLOW)
    cprint("3. High", YELLOW)
    print()
    while True:
        try:
            priority = int(handled_input("> "))
            if priority not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            cprint("Invalid Value", RED)
    upd = questable.update_quest(side_quest, qid, priority=priority)
    clear()
    if "error" in upd:
        cprint("Error changing priority", RED)
        cprint(upd["error"], RED)
    else:
        cprint("Changed priority", GREEN)


def change_difficulty(side_quest, qid):
    cprint("Choose difficulty", GREEN)
    print()
    cprint("1. Low", YELLOW)
    cprint("2. Medium", YELLOW)
    cprint("3. High", YELLOW)
    print()
    while True:
        try:
            difficulty = int(handled_input("> "))
            if difficulty not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            cprint("Invalid Value", RED)
    upd = questable.update_quest(side_quest, qid, difficulty=difficulty)
    clear()
    if "error" in upd:
        cprint("Error changing difficulty", RED)
        cprint(upd["error"], RED)
    else:
        cprint("Changed difficulty", GREEN)


def delete_quest(side_quest, qid):
    upd = questable.delete_quest(side_quest, qid)
    clear()
    if 'error' in upd:
        cprint("Could not delete " + "side " * side_quest + "quest", RED)
        cprint(upd["error"], RED)
        return
    if upd['success']:
        cprint("Deleted " + "side " * side_quest + "quest", GREEN)
    else:
        cprint("Could not delete " + "side " * side_quest + "quest", RED)


# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Questable CLI interface.",
    epilog="CLI parameters taken priority over config."
)
parser.add_argument('--api-url', '-a', help="URL for api endpoint")
parser.add_argument('--token', '-t', help="Token obtained from questable bot")
parser.add_argument('--config', '-c', help="Path to config file")
args = parser.parse_args()

config_from_args = {}
if args.api_url is not None:
    config_from_args['api_url'] = args.api_url

if args.token is not None:
    config_from_args['token'] = args.token

if args.config:
    config_file_path = os.path.expanduser(args.config)
    if not os.path.isfile(config_file_path):
        cprint("Config file does not exist", RED)
        sys.exit(2)
else:
    config_file_path = os.path.expanduser('~/.config/questable.conf')


# Parse config file
config_from_file = {}

if os.path.isfile(config_file_path):
    with open(config_file_path) as f:
        for i in f.readlines():
            i = i.strip()
            if len(i) == 0:
                continue
            if i[0] == "#":
                continue
            params = i.split("=")
            if len(params) < 2:
                continue
            config_from_file[params[0].strip()] = "=".join(params[1:]).strip()

# Merge configs
config = {**config_from_file, **config_from_args}


clear()
prompt_for_write = False
if 'api_url' not in config:
    prompt_for_write = True
    cprint("API URL not found", RED)
    cprint("Using default: https://api.questable.webionite.com", GREEN)
    print()
    config["api_url"] = "https://api.questable.webionite.com/"


if 'token' not in config:
    prompt_for_write = True
    cprint("Token not found", RED)
    print()
    cprint("Enter Token", GREEN)
    print()
    config["token"] = handled_input("> ")
    print()


questable.init(config)

cprint("Welcome to questable.", GREEN)
print()
cprint("Trying to authenticate token . . . ", GREEN)
if questable.auth():
    cprint("Authentication successful", GREEN)
    print()
else:
    cprint("Authentication failed! Please check your Token / API URL", RED)
    sys.exit(1)

# Prompt to write config settings
if prompt_for_write:
    cprint("Do you want to write config?", YELLOW)
    print()
    write_config = True if handled_input("y/N > ").lower() == "y" else False
    if write_config:
        if not os.path.isdir(os.path.dirname(config_file_path)):
            os.makedirs(os.path.dirname(config_file_path))
        with open(config_file_path, 'w') as f:
            f.write("# API URL for the questable server\n")
            f.write("api_url = " + questable.config.api_url + "\n")
            f.write("# Token provided by questable bot\n")
            f.write("token = " + questable.config.token + "\n")
    print()

while True:
    cprint("Choose an option", GREEN)
    print()
    cprint("1. Add a quest", YELLOW)
    cprint("2. Add a side quest", YELLOW)
    cprint("3. List quests", YELLOW)
    cprint("4. List side quests", YELLOW)
    cprint("5. Check status", YELLOW)
    cprint("q. Quit", YELLOW)
    print()
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
            print()
    if i == 1:
        clear()
        add_quest(False)
    elif i == 2:
        clear()
        add_quest(True)
    elif i == 3:
        clear()
        list_quest(False)
    elif i == 4:
        clear()
        list_quest(True)
    elif i == 5:
        clear()
        status()
