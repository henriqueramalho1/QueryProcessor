from state import*
from initialmenu import InitialMenu
from databasesmenu import DatabasesMenu

class DataImportMenu(State):

    def processInput(self):
        self.clearTerminal()

        print("Selecione o banco de dados:")
        print("1 - MySQL")
        print("2 - PostgreSQL")
        print("3 - Sair\n")

        option = input()

        if(option == "1"):
            self.app.changeState(InitialMenu(self.app, "MySQL"))

        elif(option == "3"):
            self.app.stop()
