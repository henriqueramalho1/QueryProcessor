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
            file_name = ''
            data = []

            if 'join' in words or 'JOIN' in words:
                data = self.join(words, databaseName)
            else:
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
        filtered_fields = []
        comparison_fields = []
        comparison_types = []
        ordered_by = []
        has_where = False
        has_modifiers = False
        has_order_by = False
        order_desc = False

        column_loaded = {column: False for column in selected_columns}

        if 'where' in words or 'WHERE' in words:
            filtered_fields = self.get_filtered_columns(words)
            comparison_fields = self.get_comparison_fields(words)
            comparison_types = self.get_comparison_types(words)
            comparison_modifiers = self.get_comparison_modifiers(words)
            if len(comparison_modifiers) != 0:
                has_modifiers = True
            has_where = True

        if ('order' in words and 'by' in words) or ('ORDER' in words and 'BY' in words):
            ordered_by = self.get_ordered_field(words)
            has_order_by = True
            if 'desc' in words or 'DESC' in words:
                order_desc = True

        if has_order_by:
            ordered_field_index = self.get_column_index(ordered_by, data_table[0])
            sorted_data = sorted(data_table[1:], key=lambda x: self.convert_type(x[ordered_field_index]), reverse= order_desc)
            data_table = [data_table[0]] + sorted_data

        selected_data = []

        selected_indexes = []
        for i, line in enumerate(data_table):
            line_mod = []
            for j, elem in enumerate(line):
                if i == 0:
                    if (line[j] in selected_columns and column_loaded[line[j]] == False) or (selected_columns[0] == '*'):
                        selected_indexes.append(True)
                        column_loaded[line[j]] = True
                        line_mod.append(line[j])
                    else:
                        selected_indexes.append(False)
                else:
                    if selected_indexes[j]:
                        line_mod.append(line[j])
            # Salva registro
            if has_where and i != 0:
                comparison_results = []
                for idx, filters in enumerate(filtered_fields):
                    column_i = self.get_column_index(filtered_fields[idx], data_table[0])
                    data1 = line[column_i]
                    data2 = comparison_fields[idx]
                    comparison_type = comparison_types[idx]
                    result = self.compare(data1, comparison_type, data2)
                    comparison_results.append(result)

                if has_modifiers:
                    final_result = self.compare(comparison_results[0], comparison_modifiers[0], comparison_results[1])
                    for j in range(2, len(comparison_results)):
                        final_result = self.compare(final_result, comparison_modifiers[j - 1], comparison_results[j])

                    if final_result:
                        selected_data.append(line_mod)

                elif comparison_results[0]:
                    selected_data.append(line_mod)
            else:
                selected_data.append(line_mod)

        return selected_data

    def convert_type(self, item):
        field = item  # Index of the field to sort by (quantity in this case)
        try:
            field_value = float(field)  # Attempt to convert to an integer
        except ValueError:
            field_value = field  # Keep the value as is if it cannot be converted to an integer

        return field_value

    def get_ordered_field(self, words):
        for i, word in enumerate(words):
            if word == 'by' or word == 'BY':
               return words[i + 1]


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
        field1 = self.convert_type(field1)
        field2 = self.convert_type(field2)
        if (comparison_type == '='):
            comparison_type = '=='
        return eval(f'field1 {comparison_type} field2')

    def get_comparison_modifiers(self, words):
        mods = []
        for i, word in enumerate(words):
            if word == 'and' or word == 'AND':
                mods.append(word.lower())
            elif word == 'or' or word == 'OR':
                mods.append(word.lower())
        return mods

    def get_comparison_types(self,words):
        types = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                types.append(words[i + 2])
            elif word == 'and' or word == 'AND' or word == 'or' or word == 'OR':
                types.append(words[i + 2])
        return types
    def get_comparison_fields(self, words):
        comparisons = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                comparisons.append(words[i + 3])
            elif word == 'and' or word == 'AND' or word == 'or' or word == 'OR':
                comparisons.append(words[i + 3])
        return comparisons

    def get_filtered_columns(self, words):
        columns = []
        for i, word in enumerate(words):
            if word == 'where' or word == 'WHERE':
                columns.append(words[i + 1])
            elif word == 'and' or word == 'AND' or word == 'or' or word == 'OR':
                columns.append(words[i + 1])
        return columns

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
    
    def join_tables_using(self, table1, table2, key):
        
        result_table = []

        table1_key_index = table1[0].index(key[0])
        table2_key_index = table2[0].index(key[0])

        result_table.append(table1[0] + table2[0][0:table2_key_index] + table2[0][table2_key_index + 1:])

        for line_table1 in table1[1:]:
            key_value = line_table1[table1_key_index]
            matching_rows = []

            for line_table2 in table2[1:]:
                if line_table2[table2_key_index] == key_value:
                    matching_rows.append(line_table2[0:table2_key_index] + line_table2[table2_key_index + 1:])

            if matching_rows:
                for matching_row in matching_rows:
                    result_table.append(line_table1 + matching_row)

        return result_table
    
    def join_tables_on(self, table1, table2, condition):
        
        result_table = []

        field1 = condition[0].split('.')[1]
        field2 = condition[2].split('.')[1]

        if (field1 in table2[0]) and (field2 in table1[0]) and (field1 not in table1[0]) and (field2 not in table2[0]):
            fieldAux = field1
            field1 = field2
            field2 = fieldAux
    
        table1_key_index = table1[0].index(field1)
        operator = condition[1]
        table2_key_index = table2[0].index(field2)

        result_table.append(table1[0] + table2[0])

        for line_table1 in table1[1:]:
            key_value = line_table1[table1_key_index]
            matching_rows = []

            for line_table2 in table2[1:]:
                if operator == "=":
                    if line_table2[table2_key_index] == key_value:
                        matching_rows.append(line_table2)
                elif operator == "<":
                    if line_table2[table2_key_index] < key_value:
                        matching_rows.append(line_table2)
                elif operator == ">":
                    if line_table2[table2_key_index] > key_value:
                        matching_rows.append(line_table2)

            if matching_rows:
                for matching_row in matching_rows:
                    result_table.append(line_table1 + matching_row)

        return result_table
    
    def join(self, words, databaseName):
        
        fields = self.get_fields(words)
        clauses = self.get_join_clauses(words)
        tables = []

        for field in fields:
            file_name = 'csv/' + str(databaseName) + '/' + field.lower() + ".csv"
            data = self.get_data(file_name)
            tables.append(data)

        result = tables[0]  # Mais de um join na query

        for i in range(1, len(tables)):
            table = tables[i]
            clause = clauses[i-1]

            if(len(clause) == 1):
                result = self.join_tables_using(result, table, clause)
            else:
                result = self.join_tables_on(result, table, clause)
            

        return result

    def get_fields(self, words):
        fields_index = [i for i, word in enumerate(words) if word == 'join' or word == 'JOIN' or word == 'from' or word == 'FROM']

        fields = []

        for index in fields_index:
            if index + 1 < len(words):
                fields.append(words[index + 1])
        
        return fields

    def get_join_clauses(self, words):

        joins_index = [i for i, word in enumerate(words) if word == 'join' or word == 'JOIN']
        valid_clauses = ['ON', 'on', 'USING', 'using']
        clauses_index = []
        clauses = []

        for i in range(len(joins_index)):

            if(i == len(joins_index) - 1):
                end = len(words)
            else:
                end = joins_index[i + 1]

            for j in range(joins_index[i], end):
                if words[j] in valid_clauses:
                    clauses_index.append(j)

        for index in clauses_index:
            if words[index] == 'using' or words[index] == 'USING':
                clauses.append([words[index + 1]])
            else:
                clauses.append([words[index + 1], words[index + 2], words[index + 3]])

        return clauses
