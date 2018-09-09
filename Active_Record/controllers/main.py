from models.user import User
from connect_db import create_connection
from hash_password import generate_salt

if __name__ == '__main__':
    user_obj = User()

    user_obj.username = 'Jan Boguchwał'
    user_obj.email = 'bogoja@gmail.com'
    user_obj.set_password('blablaBle1', generate_salt())

    cnx = create_connection('exam2')
    cursor = cnx.cursor()

    user_obj.save_to_db(cursor)
    cnx.close()
