from state import*

class InitialMenu(State):

    def processInput(self):
        self.clearTerminal()

        print("Menu Inicial")
        print("1 - Importar dados")
        print("2 - Processar queries")
        print("3 - Sair\n")

        option = input()

        if(option == "1"):
            from dataimportmenu import DataImportMenu
            self.app.changeState(DataImportMenu(self.app))
        elif(option == "3"):
            self.app.stop()