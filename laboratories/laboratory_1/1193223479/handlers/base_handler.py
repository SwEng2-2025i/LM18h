import random

class BaseHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, user, message):
        raise NotImplementedError("Subclasses must implement handle()")
