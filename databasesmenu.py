from state import*
import time
from dataimporter import DataImporter
from tablesmenu import TablesMenu

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
                databaseName = str(databasesList[int(option) - 1])
                databaseName = databaseName.split("-")
                self.app.changeState(TablesMenu(self.app, self.database, databaseName[0]))
            except:
                pass
