from user import User
from connect_db import connect

if __name__ == '__main__':
    user_obj = User()

    cnx = connect('exam2')
    cursor = cnx.cursor()

    user_obj.save_to_db(cursor)
    cnx.close()
