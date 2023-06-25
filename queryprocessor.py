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
        filtered_field = []
        comparison_field = []
        comparison_type = []

        has_where = False
        if 'where' in words or 'WHERE' in words:
            filtered_field = self.get_filtered_column(words)
            comparison_field = self.get_comparison_field(words)
            comparison_type = self.get_comparison_type(words)
            has_where = True

        columns = self.get_selected_columns(words)
        selected_data = []

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
            # Salva registro
            if has_where and i != 0:
                column_i = self.get_column_index(filtered_field, data_table[0])
                data1 = line[column_i]
                # Pode ser dado avulso ou dado de um campo
                # data2 = words[c_index]
                data2 = comparison_field
                if self.compare(data1, comparison_type, data2):
                    selected_data.append(line_mod)
            else:
                selected_data.append(line_mod)

        return selected_data


    def get_column_index(self, column, column_names):
        index = []
        for i, col in enumerate(column_names):
            if column == col:
                return i
        return -1

    def compare(self, field1, comparison_type, field2):
        comp_operators = ['=', '!=', '<', '>', '<=', '>=']

        logical_operators = ['or', 'OR', 'and', 'AND']
        if comparison_type in comp_operators:
            if comparison_type == '=':
                comparison_type = '=='
            result = eval(f"field1 {comparison_type} field2")
            return result


    def get_comparison_type(self,words):
        index = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                index = i + 2
                break
        return words[index]
    def get_comparison_field(self, words):
        index = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                index = i + 3
                break
        return words[index]

    def get_filtered_column(self, words):
        index = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                index = i + 1
                break
        return words[index]

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
