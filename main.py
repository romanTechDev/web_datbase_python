from flask import Flask, request, render_template, flash, redirect, url_for, Markup
from flask_login import LoginManager, login_user, login_required, UserMixin
import hashlib
import pymysql

import DataBase_Works
from DataBase_Works import connect_to_base
from DataBase_Works import DataBaseNetwork
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

                DataBase_Works.user_role = db_network.get_role_user(login_hash)[0][0]

                #flash('Верные данные !', category='success')
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


@app.route('/database.html', methods=['POST', 'GET'])
def database():
    if request.method == "POST":
        table_name = request.form['table_name']
        print(table_name)
        return redirect('database.html')
    else:
        tables = ''
        for row in db_network.get_rows_from_base('show tables'):
            tables += f'<option class="table_item"> {row[0]} </option>\n'

        option_tables = Markup(tables)
        db_role = DataBase_Works.user_role
        database_name = DataBase_Works.DATABASENAME

        return render_template('database.html', option_tables=option_tables, database_name=database_name, db_role=db_role)


if __name__ == '__main__':
    app.run(debug=True)
