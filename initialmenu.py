from state import*

class InitialMenu(State):

    def __init__(self, app, database):
        super().__init__(app)
        self.database = database

    def processInput(self):
        self.clearTerminal()

        print("Menu Inicial")
        print("1 - Importar dados")
        print("2 - Processar queries")
        print("3 - Voltar\n")

        option = input()

        if option == "1":
            from databasesmenu import DatabasesMenu
            self.app.changeState(DatabasesMenu(self.app, self.database))
        elif option == "2":
            from querymenu import QueryImportMenu
            self.app.changeState(QueryImportMenu(self.app, self.database))
        elif option == "3":
            from dataimportmenu import DataImportMenu
            self.app.changeState(DataImportMenu(self.app))
