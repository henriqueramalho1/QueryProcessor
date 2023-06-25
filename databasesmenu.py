from state import*
import time
from dataimporter import DataImporter

class DatabasesMenu(State):

    def __init__(self, app, database):
        super().__init__(app)
        self.database = database

    def processInput(self):
        self.clearTerminal()
        importer = DataImporter()
        databasesList =importer.getDatabasesList(self.database)
       
        for i, databaseName in enumerate(databasesList):
            print(str(i + 1) + " - " + databaseName)

        print()
        print(str(len(databasesList) + 1) + " - Voltar\n")

        option = input()
        
        if(option == str(len(databasesList) + 1)):
            from dataimportmenu import DataImportMenu
            self.app.changeState(DataImportMenu(self.app))
        else:
            try:
                #Armazena apenas o nome do database
                databaseName = str(databasesList[int(option) - 1])
                databaseName = databaseName.split("-")
                importer.load(databaseName[0])
            except:
                print("Não foi possível carregar os dados")
