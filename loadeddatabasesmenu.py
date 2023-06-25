from state import*
import os

class LoadedDatabasesMenu(State):

    def processInput(self):
        self.clearTerminal()

        print("Selecione em qual banco de dados deseja realizar a consulta")

        path = 'csv/'

        loadedDatabases = os.listdir(path)
        
        for i, database in enumerate(loadedDatabases):
            print(str(i + 1) + " - " + database)

        print()
        print(str(len(loadedDatabases) + 1) + " - Voltar\n")

        option = input()

        if(option == str(len(loadedDatabases) + 1)):
            from initialmenu import InitialMenu
            self.app.changeState(InitialMenu(self.app))
        else:
            try:
                #Armazena apenas o nome do database
                databaseName = str(loadedDatabases[int(option) - 1])
                databaseName = databaseName.split("-")
                from querymenu import QueryMenu
                self.app.changeState(QueryMenu(self.app, databaseName[0]))
            except:
                print("Não foi possível realizar a ação")