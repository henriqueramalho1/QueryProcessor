import mysql.connector
import csv
import os

class DataImporter:

    def __init__(self):
        pass

    def getDatabasesList(self, database):
        if database == "PostgreSQL":
            return self.getPostgreSQLDatabasesList()
        elif database == "MySQL":
            return self.getMySQLDatabasesList()

    def getPostgreSQLDatabasesList(self):
        pass

    def getMySQLDatabasesList(self):

        try:
            self.db = mysql.connector.connect(user="root", host="localhost", password="1234ramalho")

        except:
            return []

        cursor = self.db.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        databasesList = []

        for database in databases:
            databasesList.append(database[0])
            
        cursor.close()
        self.db.close()

        return databasesList


    def load(self, databaseName):
        self.db = mysql.connector.connect(user="root", host="localhost", password="1234ramalho", database=databaseName)

        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        table_names = [table[0] for table in cursor.fetchall()]

        for table_name in table_names :
            cursor.execute(f"SELECT * FROM {table_name};")
            results = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]
            path = "csv/" + databaseName

            if not os.path.exists(path) :
                os.makedirs(path)

            filename = f"{table_name}.csv"
            csv_filename = path + "/" + filename

            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Escrever os nomes das colunas
                writer.writerow(column_names)
                
                # Escrever os dados
                writer.writerows(results)

        cursor.close()
        self.db.close()