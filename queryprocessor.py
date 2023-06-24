import re
import csv
class QueryProcessor:

    def __init__(self, database):
        self.database = database

    def processQuery(self, databaseName, query):
        words = query.replace(',', ' ').split()
        file_name = 'csv/' + str(databaseName) + '/' + self.get_table_name(words).lower() + ".csv"

        if 'update' in words or 'UPDATE' in words:
            pass

        if 'insert' in words or 'INSERT' in words:
            pass

        if 'delete' in words or 'DELETE' in words:
            pass

        if 'select' in words or 'SELECT' in words:
            data = self.get_data(file_name)
            selected_data = self.select(data, words)
            self.print_table(selected_data)

    def get_data(self, file_name):

        data_table = []

        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for i, line in enumerate(csv_reader):
                data_table.append(line)

        return data_table

    def select(self, data_table, words):

        columns = self.get_selected_columns(words)
        selected_data_table = []

        selected_indexes = []
        for i, line in enumerate(data_table):
            line_mod = []
            for j, elem in enumerate(line):
                if i == 0:
                    if line[j] in columns or columns[0] == '*':
                        selected_indexes.append(True)
                        line_mod.append(line[j])
                    else:
                        selected_indexes.append(False)
                else:
                    if selected_indexes[j]:
                        line_mod.append(line[j])

            selected_data_table.append(line_mod)

        return selected_data_table

    def print_table(self, data_table):
        for row in data_table:
            print(row)

    def get_table_name(self, words):
        index = -1
        for i, word in enumerate(words):
            if word == 'from' or word == 'FROM':
                index = i + 1
                break

        return words[index]

    def get_selected_columns(self,words):
        columns = []
        for elem in words[1:]:
            if elem == 'from' or elem == 'FROM':
                break
            columns.append(elem)
        return columns
