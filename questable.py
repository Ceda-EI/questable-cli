import requests


class Config():
    pass


config = Config()


def init(cfg):
    global config
    config.api_url = cfg["api_url"].rstrip("/") + "/"
    config.token = cfg["token"]


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


def get_quest(side_quest, qid):
    if side_quest:
        url = config.api_url + "get_side_quest"
    else:
        url = config.api_url + "get_quest"
    parameters = {
        "token": config.token,
        "id": qid
    }
    res = requests.get(url, parameters)
    return res.json()


def player():
    url = config.api_url + "player"
    parameters = {
        "token": config.token
    }
    res = requests.get(url, parameters)
    return res.json()


def add_quest(side_quest, name, priority, difficulty):
    if side_quest:
        url = config.api_url + "add_side_quest"
    else:
        url = config.api_url + "add_quest"
    data = {
        "token": config.token,
        "name": name,
        "priority": priority,
        "difficulty": difficulty
    }
    res = requests.post(url, data=data)
    return res.json()


def update_quest(side_quest, qid, name=None, priority=None, difficulty=None,
                 state=None):
    if side_quest:
        url = config.api_url + "update_side_quest"
    else:
        url = config.api_url + "update_quest"

    data = {
        "token": config.token,
        "id": qid
    }
    if name:
        data["name"] = name
    if priority:
        data["priority"] = priority
    if difficulty:
        data["difficulty"] = difficulty
    if state:
        data["state"] = state

    res = requests.post(url, data=data)
    return res.json()


def delete_quest(side_quest, qid):
    if side_quest:
        url = config.api_url + "delete_side_quest"
    else:
        url = config.api_url + "delete_quest"

    data = {
        "token": config.token,
        "id": qid
    }

    res = requests.delete(url, data=data)
    return res.json()
