from state import*
from dataimporter import DataImporter

class TablesMenu(State):

    def __init__(self, app, database, databaseName):
        super().__init__(app)
        self.database = database
        self.databaseName = databaseName

    def processInput(self):
        self.clearTerminal()
        importer = DataImporter()
        tableList = importer.getDatabaseTableList(self.database, self.databaseName)
       
        for i, table in enumerate(tableList):
            print(str(i + 1) + " - " + table)

        print()
        print(str(len(tableList) + 1) + " - Voltar\n")

        option = input()
        
        if(option == str(len(tableList) + 1)):
            from databasesmenu import DatabasesMenu
            self.app.changeState(DatabasesMenu(self.app, self.database))
        else:
            try:
                #Armazena apenas o nome do database
                table = str(tableList[int(option) - 1])
                table = table.split("-")
                importer.load(self.database, self.databaseName, table[0])
            except:
                print("Não foi possível carregar os dados")
