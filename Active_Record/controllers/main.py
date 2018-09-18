from user import User
from connect_db import create_connection
from hash_password import generate_salt
from message import Message

if __name__ == '__main__':
    user_obj = User()

    user_obj.username = 'Jan Boguchwał'
    user_obj.email = 'bogoja@gmail.com'
    user_obj.set_password('blablaBle1', generate_salt())

    cnx = create_connection('exam2')
    cursor = cnx.cursor()

    # user_obj.save_to_db(cursor)
    obj = user_obj.load_user_by_id(cursor, 2)
    print(obj.__dict__)

    obj = user_obj.load_all_users(cursor)
    print([ob.__dict__ for ob in obj])

    a = Message.load_all_messages_for_user(cursor, 2)
    for i in a:
        print(i.text)

    cnx.close()
