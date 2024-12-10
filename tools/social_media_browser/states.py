from enum import StrEnum


class States(StrEnum):
    success = "success"
    fail = "fail"
    running = "running"
    quit = "quit"
    authenticated = "logged_in"
    not_authenticated = "not_logged_in"


class App(StrEnum):
    instagram = "instagram"
    twitter = "twitter"
