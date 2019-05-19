import requests
import config


def auth():
    url = config.api_url + "auth"
    parameters = {
        "token": config.token
    }
    res = requests.get(url, parameters)
    return res.json()["success"]


def get_quests(side_quest):
    if side_quest:
        url = config.api_url + "get_side_quests"
    else:
        url = config.api_url + "get_quests"
    parameters = {
        "token": config.token
    }
    res = requests.get(url, parameters)

    if res.status_code != 200:
        return False
    return res.json()
