#!/usr/bin/env python3

import argparse
import questable
import sys
import os
from cprint import cprint, RED

# Configure parser for top level command
parser = argparse.ArgumentParser(description="Questable CLI")
parser.add_argument(
    '--api-url',
    '-a',
    help="URL for api endpoint"
)
parser.add_argument(
    '--token',
    '-t',
    help="Token obtained from questable bot"
)

parser.add_argument(
    '--config',
    '-c',
    help="Path to config file"
)


subparsers = parser.add_subparsers(dest='subparser')


# Define function for handling list_quests
def list_quests(args):
    quests = questable.get_quests(args.side_quests)
    quests_sorted = [[], [], []]
    for q in quests:
        quests_sorted[3 - q["priority"]].append(q)

    for count, group in enumerate(quests_sorted):
        if len(group) > 0:
            print("Priority: " + ["Hard", "Medium", "Low"][count])
            print("")
            print("ID\tDiff.\tName")
        for q in group:
            print(str(q["id"]) + "\t" +
                  ["Low", "Medium", "Hard"][q["difficulty"] - 1] +
                  "\t" + q["name"])
        if len(group) > 0 and count < 2:
            print()


# Add subparser for list_quests
subparser_list_quests = subparsers.add_parser(
    'list_quests',
    description='List quests or subquests',
    aliases=['lq', 'l'],
    help="List Quests"
)
subparser_list_quests.add_argument(
    '--side-quests',
    '-s',
    action="store_true",
    help="Add side quests instead"
)
subparser_list_quests.set_defaults(func=list_quests)


# Define function for handling add_quest
def add_quest(args):
    if args.priority not in [1, 2, 3]:
        cprint("Invalid priority", RED)
        sys.exit(2)

    if args.difficulty not in [1, 2, 3]:
        cprint("Invalid difficulty", RED)
        sys.exit(2)

    q = questable.add_quest(args.side_quest, args.name, args.priority,
                            args.difficulty)
    print("ID:", q["id"])
    print("Name:", q["name"])
    print("Difficulty:", ["Low", "Medium", "Hard"][q["difficulty"] - 1])
    print("Priority:", ["Low", "Medium", "Hard"][q["priority"] - 1])
    print("State:", "Completed" if q["state"] else "Incomplete")


# Configure subparser for add_quest
subparser_add_quest = subparsers.add_parser(
    'add_quest',
    description='Add quests or subquests',
    aliases=['aq', 'a'],
    help="Add Quest"
)

subparser_add_quest.add_argument(
    '--side-quest',
    '-s',
    action="store_true",
    help="Add side quests instead"
)

subparser_add_quest.add_argument(
    '--name',
    '-n',
    required=True,
    help="Name of Quest"
)

subparser_add_quest.add_argument(
    '--priority',
    '-p',
    required=True,
    type=int,
    help="Priority of quest (1, 2, 3)"
)
subparser_add_quest.add_argument(
    '--difficulty',
    '-d',
    required=True,
    type=int,
    help="Difficulty of quest (1, 2, 3)"
)

subparser_add_quest.set_defaults(func=add_quest)


# Define function for handling update_quest
def update_quest(args):
    pass


# Configure subparser for update_quest
subparser_update_quest = subparsers.add_parser(
    'update_quest',
    description="Update quests or side quest",
    aliases=['uq', 'u'],
    help="Update Quest"
)

subparser_update_quest.add_argument(
    '--side-quest',
    '-s',
    action="store_true",
    help="Update side quests instead"
)

subparser_update_quest.add_argument(
    'id',
    help="ID of quest"
)

subparser_update_quest.add_argument(
    '--name',
    '-n',
    help="Name of Quest"
)

subparser_update_quest.add_argument(
    '--priority',
    '-p',
    type=int,
    help="Priority of quest (1, 2, 3)"
)

subparser_update_quest.add_argument(
    '--difficulty',
    '-d',
    type=int,
    help="Difficulty of quest (1, 2, 3)"
)

subparser_update_quest.add_argument(
    '--mark-as-done',
    '-m',
    action="store_true",
    help="Mark quest as done"
)

subparser_update_quest.set_defaults(func=update_quest)


# Define function for handling delete_quest
def delete_quest(args):
    pass


# Configure subparser for delete_quest
subparser_delete_quest = subparsers.add_parser(
    'delete_quest',
    description="Delete quest or side quest",
    aliases=['dq', 'd'],
    help="Delete Quest"
)

subparser_delete_quest.add_argument(
    '--side-quest',
    '-s',
    action="store_true",
    help="Add side quests instead"
)

subparser_delete_quest.add_argument(
    'id',
    help="ID of quest"
)

subparser_delete_quest.set_defaults(func=delete_quest)


# Define function for handling status
def status(args):
    player = questable.player()
    print("XP: " + str(player["xp"]))
    print("Quests: " + str(player["quests_completed"]) + "/" +
          str(player["total_quests"]))
    print("Side Quests: " + str(player["side_quests_completed"]) + "/" +
          str(player["total_side_quests"]))


# Configure subparser for status
subparser_status = subparsers.add_parser(
    'status',
    description="Get status of player",
    aliases=['s'],
    help="Get status of player"
)

subparser_status.set_defaults(func=status)

# Parse arguments
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

if 'api_url' not in config:
    cprint("API URL not found.", RED)
    sys.exit(1)
elif 'token' not in config:
    cprint("TOKEN not found", RED)
    sys.exit(1)

questable.init(config)
if not questable.auth():
    cprint("Authentication failed! Please check your Token / API URL", RED)
    sys.exit(1)

if args.subparser:
    args.func(args)
else:
    parser.print_help()
