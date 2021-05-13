import pymysql.connections

DATABASENAME = 'photocenter'


def connect_to_base():
    try:
        connected_data_base = pymysql.connect(user='root', password='root', host='localhost', database=DATABASENAME)
        return connected_data_base
    except pymysql.Error:
        print('Данные в подключении не верны/ Не подключен веб сервер !')

class DataBaseNetwork:  # Работа с данными в базе данных

    def __init__(self):
        self.connected_data_base = connect_to_base()
        self.cursor = self.connected_data_base.cursor()

    def execute_to_base(self, sql_request):
        try:
            self.cursor.execute(sql_request)
            self.connected_data_base.commit()
        except pymysql.Error:
            print('execute_to_base', 'Данные в запросе не вверны !')

    def get_rows_from_base(self, sql_request):
        try:
            self.cursor.execute(sql_request)
            rows = self.cursor.fetchall()
            return rows
        except pymysql.Error:
            print('get_rows_from_base',
                                 f'Данные в запросе не вверны !{sql_request}')

    def get_columns_table(self, table):

        columns_dirty = self.get_rows_from_base(f'show columns from {table}')

        columns = [columns[0] for columns in columns_dirty]

        return columns

    def get_rows_table(self, table):

        rows = self.get_rows_from_base(f'select * from {table}')

        return rows

    def add_row(self, table, columns_array, values_array):

        columns = ','.join(columns_array)
        values = "'" + "','".join(values_array) + "'"

        self.execute_to_base(f'INSERT INTO {table}({columns}) VALUES({values})')
        print(f'db_add_row', f'УСПЕШНАЯ ЗАПИСЬ !\nINSERT INTO {table}({columns}) VALUES({values})')

    def add_row_hash(self, table, columns_array, hash_sums_array):

        columns = ','.join(columns_array)
        hash_sums = "'" + "','".join(hash_sums_array) + "'"

        self.execute_to_base(f'INSERT INTO {table}({columns}) VALUES({hash_sums})')

    def modify_row(self, table, columns_values_array, id_row):

        data = ''
        counter = 0
        while counter != len(columns_values_array):
            data += f"{columns_values_array[counter]}="
            counter += 1
            data += f"'{columns_values_array[counter]}',"
            counter += 1

        self.execute_to_base(f'UPDATE {table} SET {data[0:-1]} WHERE ID_{table} = "{id_row}"')

        print(f'db_modify_row', f'УСПЕШНАЯ ЗАПИСЬ !\nUPDATE {table} SET {data[0:-1]} '
                                              f'WHERE ID_{table} = "{id_row}"')

    def delete_row(self, table, id_row):

        self.execute_to_base(f'DELETE FROM {table} WHERE ID_{table} = "{id_row}"')
        print(f'db_delete_row', f'УСПЕШНОЕ УДАЛЕНИЕ !\nDELETE FROM {table} WHERE ID_{table} = "{id_row}"')

    def __del__(self):
        self.connected_data_base.close()
