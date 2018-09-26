import argparse
from controllers.connect_db import create_connection
from models.message import Message
from models.user import User
from controllers.hash_password import check_password


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest='username', help="User login")
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-t", "--to", dest='to', help="Receiver of message email")
    parser.add_argument("-l", "--list", dest='list', action='store_true', help="List all users")
    parser.add_argument("-s", "--send", dest='send', help="write and send message")

    options, unknown = parser.parse_known_args()
    return options


def scenario(options):
    cnx = create_connection('exam2')
    cursor = cnx.cursor()

    if options.username and options.password and options.list and not options.to and not options.send:
        if options.username and options.password and options.list and not options.to and not options.send:
            user = User.load_user_by_name(cursor, options.username)
            if user is not None:
                password = user.hashed_password
                if check_password(options.password, password):
                    messages = Message.load_all_messages_for_user(cursor, user.id)

                    for message in messages:
                        for key, value in message.__dict__.items():
                            if key != '_Message__hashed_password':
                                key = 'Message Id' if key == '_Message__id' else key
                                print('{}: {}'.format(key, value), end='\n')
                        print('\n')
                else:
                    print('Podane hasło jest błędne')
            else:
                print('Podany użytkownik nie istnieje')

    elif options.username and options.password and options.to and options.send and not options.list:
        user = User.load_user_by_name(cursor, options.username)
        user_to = User.load_user_by_mail(cursor, options.to)
        if user is not None and user_to is not None:
            password = user.hashed_password
            if check_password(options.password, password):
                if options.send != '':
                    msg = Message()
                    msg.from_id = user.id
                    msg.to_id = user_to.id
                    msg.text = options.send
                    msg.save_to_db(cursor)
                    print('Wiadomość została wysłana do {} na email {} o treści: \n"{}"'.format(user_to.username, user_to.email, msg.text))
            else:
                print('Podane hasło jest błędne')
        else:
            if user is None:
                print("Zły login, proszę podac wlasciwą nazwę użytkownika")
            elif user_to is None:
                print("Uzytkownik o podanym mailu nie istnieje")

    else:
        print('Brak funkcjonalnosci dla podanych parametrów')

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    scenario(set_options())
