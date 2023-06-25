from initialmenu import InitialMenu

class App:

    def __init__(self):
        self.state = InitialMenu(self)
        self.quit = False

    def changeState(self, newState):
        self.state = newState

    def stop(self):
        self.quit = True

    def run(self):
        while not self.quit:
            self.state.processInput()