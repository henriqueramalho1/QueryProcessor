from state import*
from databasesmenu import DatabasesMenu

class DataImportMenu(State):

    def processInput(self):
        self.clearTerminal()

        print("Selecione o banco de dados:")
        print("1 - MySQL")
        print("2 - PostgreSQL")
        print("3 - Voltar\n")

        option = input()

        if(option == "1"):
            self.app.changeState(DatabasesMenu(self.app, "MySQL"))

        elif(option == "2"):
            self.app.changeState(DatabasesMenu(self.app, "PostgreSQL"))

        elif(option == "3"):
            from initialmenu import InitialMenu
            self.app.changeState(InitialMenu(self.app))
