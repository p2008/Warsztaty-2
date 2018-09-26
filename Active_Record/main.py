from controllers.connect_db import create_connection
from models.message import Message
from models.user import User


if __name__ == '__main__':

    cnx = create_connection('exam2')
    cursor = cnx.cursor()

    user_obj = User()
    #
    # user_obj.username = 'Jan Boguchwał'
    # user_obj.email = 'bogoja@gmail.com'
    # user_obj.set_password('blablaBle1', generate_salt())
    #
    # # user_obj.save_to_db(cursor)

    obj = user_obj.load_user_by_id(cursor, 2)
    print(obj.__dict__)

    obj = user_obj.load_all_users(cursor)
    print([ob.__dict__ for ob in obj])

    message_obj = Message()
    # message_obj.from_id = 3
    # message_obj.to_id = 1
    # message_obj.text = 'ta wiadmość jest od id 3 do id 1'
    #
    # a = message_obj.save_to_db(cursor)

    print('all user messages by user')
    a = message_obj.load_all_messages_for_user(cursor, 1, 2)
    for i in a:
        print(i.__dict__)

    print('\nall_messages')
    a = message_obj.load_all_messages(cursor)
    for i in a:
        print(i.__dict__)

    print('\nuser_messages by id')
    a = message_obj.load_message_by_id(cursor, 3)
    print(a.__dict__)

    print('\nget id')
    print(a.get_id)

    # a.delete(cursor)

    print('\nall_messages')
    a = message_obj.load_all_messages(cursor)
    for i in a:
        print(i.__dict__)

    cursor.close()
    cnx.close()


