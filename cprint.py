RED = "\033[38;5;1m"
GREEN = "\033[38;5;2m"
YELLOW = "\033[38;5;3m"
BLUE = "\033[38;5;4m"
MAGENTA = "\033[38;5;5m"
CYAN = "\033[38;5;6m"
WHITE = "\033[38;5;7m"
RESET = "\033[0;5;0m"


def cprint(text, color):
    print(color + text + RESET)
