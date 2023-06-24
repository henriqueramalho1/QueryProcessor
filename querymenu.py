from state import*
from queryprocessor import QueryProcessor
from dataimporter import DataImporter

class QueryImportMenu(State):

    def __init__(self, app, database):
        super().__init__(app)
        self.database = database

    def processInput(self):
        #self.clearTerminal()

        importer = DataImporter()
        databasesList = importer.getDatabasesList(self.database)

        for i, databaseName in enumerate(databasesList):
            print(str(i + 1) + " - " + databaseName)

        print()
        print(str(len(databasesList) + 1) + " - Voltar\n")

        option = input()
        databaseName = ""

        if (option == str(len(databasesList) + 1)):
            from dataimportmenu import DataImportMenu
            self.app.changeState(DataImportMenu(self.app))
        else:
            databaseName = str(databasesList[int(option) - 1])
            databaseName = databaseName.split("-")

        print("Digite a query:")

        query = input()

        processor = QueryProcessor(self.database)
        processor.processQuery(databaseName[0], query)
