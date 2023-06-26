import mysql.connector
import psycopg2
import csv
import os
from dotenv import load_dotenv
load_dotenv()

class DataImporter:

    def __init__(self):
        pass

    def getDatabasesList(self, database):
        if database == "PostgreSQL":
            return self.getPostgreSQLDatabasesList()
        elif database == "MySQL":
            return self.getMySQLDatabasesList()

    def getPostgreSQLDatabasesList(self):
        try:
            host = os.environ.get('HOST_POSTGRESQL')
            user = os.environ.get('USER_POSTGRESQL')
            port = os.environ.get('PORT_POSTGRESQL')
            pssw= os.environ.get('PASSWORD_POSTGRESQL')
            db = psycopg2.connect(user=user, host=host, password=pssw, port=port)

        except:
            return []
        
        cursor = db.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        databasesList = []

        for database in databases:
            databasesList.append(database[0])
            
        cursor.close()
        db.close()

        return databasesList

    def getMySQLDatabasesList(self):

        try:
            host = os.environ.get('HOST_MYSQL')
            user = os.environ.get('USER_MYSQL')
            port = os.environ.get('PORT_MYSQL')
            pssw= os.environ.get('PASSWORD_MYSQL')
            db = mysql.connector.connect(user=user, host=host, password=pssw, port=port)

        except:
            return []

        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        databasesList = []

        for database in databases:
            databasesList.append(database[0])
            
        cursor.close()
        db.close()

        return databasesList


    def load(self, sgbd, databaseName):
        
        db = -1
        cursor = -1
        table_names = []

        if sgbd == "MySQL":
            host = os.environ.get('HOST_MYSQL')
            user = os.environ.get('USER_MYSQL')
            port = os.environ.get('PORT_MYSQL')
            pssw= os.environ.get('PASSWORD_MYSQL')
            db = mysql.connector.connect(user=user, host=host, password=pssw, port=port, database=databaseName)
            cursor = db.cursor()
            cursor.execute("SHOW TABLES")
        else:
            host = os.environ.get('HOST_POSTGRESQL')
            user = os.environ.get('USER_POSTGRESQL')
            port = os.environ.get('PORT_POSTGRESQL')
            pssw= os.environ.get('PASSWORD_POSTGRESQL')
            db = psycopg2.connect(user=user, host=host, password=pssw, port=port, database=databaseName)
            cursor = db.cursor()
            cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")

        table_names = [table[0] for table in cursor.fetchall()]
        
        for table_name in table_names :
            cursor.execute(f'SELECT * FROM {table_name};')
            results = cursor.fetchall()

            column_names = [description[0].lower() for description in cursor.description]
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
        db.close()