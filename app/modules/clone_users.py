from . import  database
from django.contrib.auth.models import User

class CloneUserAccounts:
    def __init__(self) -> None:
        try:
            self.db_conn = database.get_mysql_connection()
        except Exception as e:
            print('existing, cannot get DB connection\nerror ', e)
            return 0
        else:
            self.db_cur = self.db_conn.cursor()
            print('Connection with db successful')
    
    def get_users_list(self):
        print('in get users')
        query = """
        SELECT name, username FROM users
        WHERE role_id = 4
        """
        self.db_cur.execute(query)
        user_data = self.db_cur.fetchall()
        user_list = [user for user in user_data if user is not None]
        if user_list:
            return user_list
        else:
            print('no data for users found')
            return 0
        # print(user_list)

    def klone_users(self):
        print('klonning users')
        data = self.get_users_list()
        for record in data:
            # username = username_obj.username
            if not User.objects.filter(username=record[1]).exists():
                password = record[1]

                # Create a user with is_staff set to False
                user = User.objects.create_user(username=record[1], password=password, is_staff=False)
                user.first_name = record[0]
                user.save()

if __name__=='__main__':
    clone_users = CloneUserAccounts()
    clone_users.klone_users()