import csv

class QueryProcessor:

    def __init__(self, database):
        self.database = database

    def processQuery(self, databaseName, query):
        words = query.replace(',', ' ').replace('(', ' ').replace(')', ' ').replace('\'', ' ').replace('\"', ' ').split()
        file_name = []

        if 'update' in words or 'UPDATE' in words:
            file_name = 'csv/' + str(databaseName) + '/' + words[1].lower() + ".csv"
            data = self.get_data(file_name)
            fields_to_update = self.get_updated_fields(words)
            selected_data = self.select(data, words, '*')
            fields_to_update_indexes = self.get_columns_indexes(fields_to_update, selected_data.pop(0))
            values = self.get_updated_values(words)
            indexes = self.get_csv_rows_indexes(selected_data, file_name)
            self.update_fields(file_name, fields_to_update_indexes, values, indexes)

        if 'insert' in words or 'INSERT' in words:
            file_name = 'csv/' + str(databaseName) + '/' + self.get_insert_table(words).lower() + ".csv"
            new_row = self.get_row_values(words)
            self.write_new_row(file_name, new_row)

        if 'delete' in words or 'DELETE' in words:
            file_name = 'csv/' + str(databaseName) + '/' + self.get_table_name(words).lower() + ".csv"
            data = self.get_data(file_name)
            selected_data = self.select(data, words, '*')
            selected_data.pop(0)  # Remove linha de nomes das colunas
            indexes = self.get_csv_rows_indexes(selected_data, file_name)
            self.delete_rows(indexes, file_name)

        if 'select' in words or 'SELECT' in words:
            file_name = 'csv/' + str(databaseName) + '/' + self.get_table_name(words).lower() + ".csv"
            data = self.get_data(file_name)
            columns = self.get_selected_columns(words)
            selected_data = self.select(data, words, columns)
            self.print_table(selected_data)

    def get_data(self, file_name):

        data_table = []

        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for i, line in enumerate(csv_reader):
                data_table.append(line)

        return data_table

    def select(self, data_table, words, selected_columns):
        filtered_field = []
        comparison_field = []
        comparison_type = []

        has_where = False
        if 'where' in words or 'WHERE' in words:
            filtered_field = self.get_filtered_column(words)
            comparison_field = self.get_comparison_field(words)
            comparison_type = self.get_comparison_type(words)
            has_where = True

        selected_data = []

        selected_indexes = []
        for i, line in enumerate(data_table):
            line_mod = []
            for j, elem in enumerate(line):
                if i == 0:
                    if line[j] in selected_columns or selected_columns[0] == '*':
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

    def get_columns_indexes(self, columns, column_names):
        indexes = []
        for i, column in enumerate(columns):
            for j, col in enumerate(column_names):
                if col == column:
                    indexes.append(j)

        return indexes

    def update_fields(self, file_name, fields_to_update_indexes, values, indexes):
        rows = []
        updated_rows = []
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            rows = list(reader)

        for idx, row in enumerate(rows):
            if idx + 1 in indexes:
                updated_row = []
                for j, field in enumerate(row):
                    if j in fields_to_update_indexes:
                        updated_row.append(values[fields_to_update_indexes.index(j)])
                    else:
                        updated_row.append(field)
                updated_rows.append(updated_row)

        with open(file_name, 'w', newline='') as new_csvfile:
            writer = csv.writer(new_csvfile, delimiter=';')
            i = 0
            for idx, row in enumerate(rows):
                if idx + 1 not in indexes:
                    writer.writerow(row)
                else:
                    writer.writerow(updated_rows[i])
                    i += 1

    def get_updated_fields(self, words):
        fields = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                return fields
            if word == '=':
                fields.append(words[i - 1])

        return fields

    def get_updated_values(self, words):
        values = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                return values
            if word == '=':
                values.append(words[i + 1])

        return values

    def delete_rows(self, indexes, file_name):
        rows = []
        new_rows = []
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            rows = list(reader)

        for idx, row in enumerate(rows):
            if idx + 1 not in indexes:
                new_rows.append(row)

        with open(file_name, 'w', newline='') as new_csvfile:
            writer = csv.writer(new_csvfile, delimiter=';')
            writer.writerows(new_rows)

    def get_csv_rows_indexes(self, data, file_name):
        indexes = []
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for i, line in enumerate(reader, 1):
                if line in data:
                    indexes.append(i)
        return indexes

    def write_new_row(self, file_name, values):
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(values)

    def get_row_values(self, words):
        values = []
        start = False
        for i, word in enumerate(words):
            if start:
                values.append(word)
            if word == 'values' or word == 'VALUES':
                start = True

        return values

    def get_insert_table(self,words):
        index = []
        for i, word in enumerate(words):
            if word == 'insert' or word == 'INSERT':
                index = i + 2
                break
        return words[index]

    def get_column_index(self, column, column_names):
        index = []
        for i, col in enumerate(column_names):
            if column == col:
                return i
        return -1

    def compare(self, field1, comparison_type, field2):
        field1 = float(field1)
        field2 = float(field2)
        if comparison_type == '=':
            if field1 == field2:
                return True
        elif comparison_type == '!=':
            if field1 != field2:
                return True
        elif comparison_type == '=':
            if field1 == field2:
                return True
        elif comparison_type == '>':
            if field1 > field2:
                return True
        elif comparison_type == '<':
            if field1 < field2:
                return True
        elif comparison_type == '>=':
            if field1 >= field2:
                return True
        elif comparison_type == '<=':
            if field1 <= field2:
                return True
        return False

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
        lengths = [max(len(str(dado)) for dado in column) for column in zip(*data_table)]

        print("+" + "+".join("-" * (length + 2) for length in lengths) + "+")

        for row in data_table:
            for data, length in zip(row, lengths):
                print(f"| {str(data):<{length}} ", end="")
            print("|")
            print("+" + "+".join("-" * (length + 2) for length in lengths) + "+")

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
