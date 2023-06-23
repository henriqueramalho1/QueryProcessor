from initialmenu import InitialMenu

class App:

    def __init__(self):
        self.state = InitialMenu(self)

    def changeState(self, newState):
        self.state = newState

    def run(self):
        self.state.processInput()