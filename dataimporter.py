import MySQLdb
import csv

class DataImporter:

    def __init__(self, database):
        self.db = MySQLdb.connect("localhost", "root", "1234", database)

    def load(self):
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        table_names = [table[0] for table in cursor.fetchall()]

        for table_name in table_names :
            cursor.execute(f"SELECT * FROM {table_name};")
            results = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            csv_filename = f"{table_name}.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escrever os nomes das colunas
                writer.writerow(column_names)
                
                # Escrever os dados
                writer.writerows(results)
    