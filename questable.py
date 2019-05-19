import requests
import config


def auth():
    url = config.api_url + "auth"
    parameters = {
        "token": config.token
    }
    res = requests.get(url, parameters)
    return res.json()["success"]
