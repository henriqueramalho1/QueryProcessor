import os

class State:

    def __init__(self, app):
        self.app = app

    def processInput(self):
        pass

    def clearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')