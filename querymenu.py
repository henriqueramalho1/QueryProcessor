from state import*
from queryprocessor import QueryProcessor

class QueryMenu(State):

    def __init__(self, app, database):
        super().__init__(app)
        self.database = database
        self.quit = False

    def processInput(self):

        self.clearTerminal()

        while not self.quit:
            print()
            print("Digite a query:")
            query = input()
            if query == "exit":
               self.quit = True 
            else:
                print()
                processor = QueryProcessor(self.database)
                try:
                    processor.processQuery(self.database, query)
                except:
                    pass
        
        from loadeddatabasesmenu import LoadedDatabasesMenu
        self.app.changeState(LoadedDatabasesMenu(self.app))
