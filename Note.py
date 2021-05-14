table_view_markup = ''
table_inputs_markup = ''
add_button_markup = ''
buttons_markup = ''
access_input_markup = ''
id_row = ''
table_name = ''

'''try:  # Удаление строки таблицы
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

        access_input = '<input type="submit" class="add_button" name="access_modify" value="Изменить">'
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
    print('Add has not posted') '''