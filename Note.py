table_view_markup = ''
table_inputs_markup = ''
add_button_markup = ''
buttons_markup = ''
access_input_markup = ''
id_row = ''
table_name = ''

'''from flask_login import LoginManager, login_user, login_required, UserMixin

class user (db_network.connected_data_base, UserMixin, login_hash):
    userId = db_network.get_rows_from_base(
        f"select ID_clientauth from clientauth where clientlogin = '{login_hash}'")
    login = db_network.get_rows_from_base(
                    f"select clientlogin from clientauth where clientlogin = '{login_hash}'")
    password = db_network.get_rows_from_base(
                        f"select clientpass from clientauth where clientpass = '{password_hash}'") <form method="post" ' \
                           'name="modify_button"><input type="submit" class="button" name="modify_button" ' \
                           'value="Изменить запись"></form> <form method="post" name="add_button"><input type="submit" ' \
                           'class="button" name="add_button" value="Добавить запись"></form>
                            <input type=text class="table_input" name="data_input" placeholder="Tipzdanie">
           <input type=text class="table_input" name="data_input" placeholder="Adres">
           <input type=text class="table_input" name="data_input" placeholder="Rabochiemesta">
           <input type="submit" class="button" name="modify_button" value="Изменить запись">
           <input type="submit" class="button" name="add_button" value="Добавить запись">'''