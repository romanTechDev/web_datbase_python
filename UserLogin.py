class UserLogin:

    def from_db(self, user_id, database):
        self.__user = database.get_rows_from_base(
            f"select clientlogin from clientauth where ID_clientauth = '{user_id}'")
        return self

    def create(self, user_id):
        self.__user = user_id
        return self

    def is_authentificated(self):
        return True

    def is_active(self):
        return True

    def is_anonumous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
