from state import*
from queryprocessor import QueryProcessor

class QueryMenu(State):

    def __init__(self, app, database):
        super().__init__(app)
        self.database = database

    def processInput(self):

        self.clearTerminal()

        while 1:
            print()
            print("Digite a query:")
            query = input()
            if query == "exit":
                from loadeddatabasesmenu import LoadedDatabasesMenu
                self.app.changeState(LoadedDatabasesMenu(self.app))
            else:
                print()
                processor = QueryProcessor(self.database)
                processor.processQuery(self.database, query)
        
