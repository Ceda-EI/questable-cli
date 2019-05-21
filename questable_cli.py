#!/usr/bin/env python3

import argparse

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


subparsers = parser.add_subparsers()

# Add subparser for list_quests
subparser_list_quests = subparsers.add_parser(
    'list_quests',
    description='List quests or subquests',
    help="List Quests"
)
subparser_list_quests.add_argument(
    '--side-quests',
    '-s',
    action="store_true",
    help="Add side quests instead"
)


# Configure subparser for add_quest
subparser_add_quest = subparsers.add_parser(
    'add_quest',
    description='Add quests or subquests',
    help="Add Quest"
)

subparser_add_quest.add_argument(
    '--side-quests',
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
    help="Difficulty of quest (1, 2, 3)"
)


# Configure subparser for update_quest
subparser_update_quest = subparsers.add_parser(
    'update_quest',
    description="Update quests or side quest",
    help="Update Quest"
)

subparser_update_quest.add_argument(
    '--side-quests',
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
    help="Difficulty of quest (1, 2, 3)"
)

subparser_update_quest.add_argument(
    '--mark-as-done',
    '-m',
    action="store_true",
    help="Mark quest as done"
)

# Configure subparser for delete_quest
subparser_delete_quest = subparsers.add_parser(
    'delete_quest',
    description="Delete quest or side quest",
    help="Delete Quest"
)

subparser_delete_quest.add_argument(
    '--side-quests',
    '-s',
    action="store_true",
    help="Add side quests instead"
)

subparser_delete_quest.add_argument(
    'id',
    help="ID of quest"
)

# Configure subparser for status
subparser_status = subparsers.add_parser(
    'status',
    description="Get status of player",
    help="Get status of player"
)

# Parse arguments
parser.parse_args()
