from flask import Flask, request, render_template, flash, redirect, url_for, Markup
from flask_login import LoginManager, login_user, login_required, UserMixin
import hashlib
import pymysql

import DataBase_Networks
from DataBase_Networks import connect_to_base
from DataBase_Networks import DataBaseNetwork
import Note
from UserLogin import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jijwiajdiwaj9ji2j2hhnwa989jkmxzlpppwq2'
# login_manager = LoginManager(app)

connect_to_base()

db_network = DataBaseNetwork()


# user_login = UserLogin()


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/authentication.html', methods=['POST', 'GET'])
def authentication():
    if request.method == "POST":
        try:

            login_name = request.form['login_input']
            login_byte = login_name.encode('utf-8')
            login_hash = hashlib.sha256(login_byte).hexdigest()

            password_name = request.form['password_input']
            password_byte = password_name.encode('utf-8')
            password_hash = hashlib.sha256(password_byte).hexdigest()

            access_data = 0

            if db_network.get_rows_from_base(
                    f"select clientlogin from clientauth where clientlogin = '{login_hash}'"):  # Авторизация в БД

                access_data += 1
                if db_network.get_rows_from_base(
                        f"select clientpass from clientauth where clientpass = '{password_hash}'"):
                    access_data += 1

            if access_data == 2:  # Доступ получен данные верны
                ''' userId = db_network.get_rows_from_base(
                    f"select ID_clientauth from clientauth where clientlogin = '{login_hash}'")
                userId = userId[0][0]
                print(userId)
                
                user_login_class = UserLogin()
                user_login = user_login_class.create(userId)
                login_user(user_login)'''

                DataBase_Networks.user_role = db_network.get_role_user(login_hash)[0][0]

                # flash('Верные данные !', category='success')
                return redirect('database.html')
            else:
                flash('Неккоректные данные !', category='error')
                return render_template('authentication.html')

        except Exception:
            return render_template('authentication.html')
    else:
        return render_template('authentication.html')


'''@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return user_login.from_db(user_id, db_network)


@app.route("/database/<alias>")
@login_required
def database(alias):
    return render_template('database.html')'''


class DataBaseWorks:
    pass

    def __init__(self):
        self.table_view = Note.table_view_markup
        self.table_name = Note.table_name
        self.table_inputs = Note.table_inputs_markup
        self.add_button = Note.add_button_markup
        self.buttons = Note.buttons_markup
        self.id_row = Note.id_row
        self.access_input = Note.access_input_markup
        pass

    def delete_row(self):  # Удаление строки таблицы
        try:
            if request.form['delete_button']:
                row = request.form['table_view']
                row = row.split(',')
                self.id_row = row[0][1:]  # Срезать скобку первого элемента
                # print('Click to delete ! ' + f"Data to delete {Note.id_row}")

                db_network.delete_row(self.table_name, self.id_row)
                return redirect('database.html')
        except Exception:
            print('Delete has not posted')

    def modify_row(self):  # Изменение строки таблицы
        try:
            if request.form['access_modify']:
                data_array = request.form.getlist('data_input')
                print(f'Click to modify ! Your Data please work with it {data_array}')

                data_to_request = []

                i = 0
                counter = 0

                for column in db_network.get_columns_table(self.table_name):
                    if counter == 0:
                        counter += 1
                        continue
                    data_to_request.append(column)
                    while i != len(data_array):
                        data_to_request.append(data_array[i])
                        i += 1
                        break

                print(data_to_request)
                db_network.modify_row(self.table_name, data_to_request, self.id_row)

                return redirect('database.html')
        except Exception:
            print('Не нажата кнопка подтверждения !!')

    def add_row(self):  # Добавление строки таблицы
        try:
            if request.form['add_button']:
                data_array = request.form.getlist('data_input')

                print(f'Click to add ! Your Data please work with it {data_array}')

                all_columns = db_network.get_columns_table(self.table_name)[1:]

                if self.table_name == 'clientauth':
                    hash_data_to_request = []
                    i = 0

                    while i != len(data_array):
                        if i == len(data_array) - 1:
                            hash_data_to_request.append(data_array[i])
                            i += 1
                        else:
                            byte_data = data_array[i].encode('utf-8')
                            hash_obj = hashlib.sha256(byte_data).hexdigest()
                            hash_data_to_request.append(hash_obj)
                            i += 1

                        print(hash_data_to_request)
                    db_network.add_row_hash(Note.table_name, all_columns, hash_data_to_request)
                else:
                    data_to_request = []
                    for data in data_array:
                        data_to_request.append(data)

                    db_network.add_row(self.table_name, all_columns, data_to_request)
        except Exception:
            print('Add has not posted')

    def __del__(self):
        flash('Опперация успешно выполнена !', category='success')
        Note.table_view_markup = ''
        Note.table_name = ''
        Note.table_inputs_markup = ''
        Note.add_button_markup = ''
        Note.buttons_markup = ''
        Note.id_row = ''
        Note.access_input_markup = ''
        pass


@app.route('/database.html', methods=['POST', 'GET'])
def database():
    if request.method == "POST":

        try:  # Выбор таблицы и дальнейшая обработка
            if request.form['table_name']:
                Note.table_name = request.form['table_name']

                data = ''
                table_inputs = ''
                counter = 0

                for row in db_network.get_rows_from_base(
                        f'select * from {Note.table_name}'):  # Данные таблицы для select
                    data += f'<option class="data_item"> {row} </option>'

                Note.table_view_markup = Markup(data)

                for column in db_network.get_columns_table(Note.table_name):  # Поля ввода данных в таблицу
                    if counter == 0:
                        counter += 1
                        continue
                    table_inputs += f'<input type=text class="table_input" name="data_input" placeholder="{column}">'

                add_button = '<input type="submit" class="button" name="add_button" value="Добавить запись">'

                Note.table_inputs_markup = Markup(table_inputs)
                Note.add_button_markup = Markup(add_button)

                buttons = '<input type="submit" class="button" name="delete_button" value="Удалить запись"> ' \
                          '<input type="submit" class="button" name="modify_button" value="Изменить запись"> '
                Note.buttons_markup = Markup(buttons)

                return redirect('database.html')
        except Exception:
            print('Table has not choose !')

        try:  # Удаление строки таблицы
            if request.form['delete_button']:
                row = request.form['table_view']
                row = row.split(',')
                print(row)
                id_row = row[0][1:]  # Срезать скобку первого элемента

                print('Click to delete ! ' + f"Data to delete {id_row}")

                db_network.delete_row(Note.table_name, id_row)

                Note.table_inputs_markup = None
                Note.table_view_markup = None
                Note.buttons_markup = None
                flash('Опперация успешно выполнена !', category='success')
                return redirect('database.html')
        except Exception:
            print('Delete has not posted')

        try:  # Изменение строки таблицы

            try:
                if request.form['access_modify']:
                    data_array = request.form.getlist('data_input')
                    print(f'Click to modify ! Your Data please work with it {data_array}')

                    data_to_request = []

                    i = 0
                    counter = 0

                    for column in db_network.get_columns_table(Note.table_name):
                        if counter == 0:
                            counter += 1
                            continue
                        data_to_request.append(column)
                        while i != len(data_array):
                            data_to_request.append(data_array[i])
                            i += 1
                            break

                    print(data_to_request)
                    db_network.modify_row(Note.table_name, data_to_request, Note.id_row)

                    return redirect('database.html')
            except Exception:
                print('Не нажата кнопка подтверждения !!')

            if request.form['modify_button'] and request.form['table_view']:
                print(Note.table_name)

                row = request.form['table_view']
                row = row.split(',')
                id_row = row[0][1:]  # Срезать скобку первого элемента
                Note.id_row = id_row
                i = 0
                table_inputs = ''
                db_row = db_network.get_rows_from_base(
                    f'select * from {Note.table_name} where ID_{Note.table_name} = "{id_row}"')[0]

                while i != len(db_row):  # Поля ввода данных в таблицу
                    print(db_row[i])
                    if i == 0:
                        i += 1
                        continue
                    table_inputs += f'<input type=text class="table_input" name="data_input" placeholder="{db_row[i]}">'
                    i += 1

                Note.table_inputs_markup = Markup(table_inputs)

                access_input = '<input type="submit" name="access_modify" value="Изменить">'
                Note.access_input_markup = Markup(access_input)
                Note.add_button_markup = None

                return redirect('database.html')

        except Exception:
            print('Modify has not posted or row wasnt choose !!')

        try:  # Добавление строки таблицы
            if request.form['add_button']:
                data_array = request.form.getlist('data_input')

                print(f'Click to add ! Your Data please work with it {data_array}')

                all_columns = db_network.get_columns_table(Note.table_name)[1:]

                if Note.table_name == 'clientauth':
                    hash_data_to_request = []
                    i = 0

                    while i != len(data_array):
                        if i == len(data_array) - 1:
                            hash_data_to_request.append(data_array[i])
                            i += 1
                        else:
                            byte_data = data_array[i].encode('utf-8')
                            hash_obj = hashlib.sha256(byte_data).hexdigest()
                            hash_data_to_request.append(hash_obj)
                            i += 1

                        print(hash_data_to_request)
                    db_network.add_row_hash(Note.table_name, all_columns, hash_data_to_request)
                else:
                    data_to_request = []
                    for data in data_array:
                        data_to_request.append(data)

                    db_network.add_row(Note.table_name, all_columns, data_to_request)

                    Note.table_inputs_markup = None
                    Note.table_view_markup = None
                    Note.buttons_markup = None
                    flash('Опперация успешно выполнена !', category='success')
        except Exception:
            print('Add has not posted')

        return redirect('database.html')

    else:  # Загрузка страницы
        tables = ''
        for row in db_network.get_rows_from_base('show tables'):
            tables += f'<option class="table_item" size="40"> {row[0]} </option>\n'

        db_role = DataBase_Networks.user_role
        database_name = DataBase_Networks.DATABASENAME

        option_tables = Markup(tables)
        table_view = Note.table_view_markup
        table_name = Note.table_name
        table_inputs = Note.table_inputs_markup
        add_input = Note.add_button_markup
        buttons = Note.buttons_markup
        id_row = Note.id_row
        access_input = Note.access_input_markup

        return render_template('database.html', option_tables=option_tables, database_name=database_name,
                               db_role=db_role, table_view=table_view, table_name=table_name, buttons=buttons,
                               table_inputs=table_inputs, add_input=add_input, id_row=id_row, access_input=access_input)


if __name__ == '__main__':
    app.run(debug=True)
