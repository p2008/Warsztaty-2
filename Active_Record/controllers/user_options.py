import argparse
from controllers.connect_db import create_connection
from models.user import User
from controllers.hash_password import check_password


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest='username', help="User login")
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-n", "--new-pass", dest='newpass', help="User new password")
    parser.add_argument("-l", "--list", dest='list', action='store_true', default=False, help="List all users")
    parser.add_argument("-d", "--delete", dest='delete', action='store_true', help="Delete user")
    parser.add_argument("-e", "--edit", dest='edit', action='store_true', default=False, help="Change user login")

    options, unknown = parser.parse_known_args()
    return options


def scenario(options):
    cnx = create_connection('exam2')
    cursor = cnx.cursor()
    user_obj = User()
    user = None
    password = None
    newpass = None

    if options.newpass:
        if len(options.newpass) >= 3:
            newpass = options.newpass
        else:
            print('hasło za krótkie. Min 3 znaki')

    if (options.username and options.password) and (not options.edit and not options.delete):
        if user_obj.load_user_by_name(cursor, options.username) is not None:
            password = user_obj.load_user_by_name(cursor, options.username).hashed_password
            if check_password(options.password, password):
                email = user_obj.load_user_by_name(cursor, options.username).email
                if email is not None:
                    print(f"Użytkownik o email: {email} już istnieje")
            else:
                print("Podane hasło jest błędne")
        else:
            user_obj.username = options.username
            user_obj.email = input('Podaj mail:\n')
            user_obj.set_password(options.password, salt=None)
            user_obj.save_to_db(cursor)

    elif options.username and options.password and options.edit:
        user = user_obj.load_user_by_name(cursor, options.username)
        password = user.hashed_password
        if check_password(options.password, password):
            if newpass is not None:
                    user.set_password(options.newpass, salt=None)
                    user.save_to_db(cursor)
                    print('nowe hasło ustawione')
            else:
                print('Ustaw właściwe hasło w przełączniku -n')
        else:
            print('Hasło niepoprawne')

    elif options.username and options.password and options.delete:
        user = user_obj.load_user_by_name(cursor, options.username)
        if user is not None:
            password = user.hashed_password
            if check_password(options.password, password):
                user_delete = input('Użytkownik: {} o email: {} zostanie usunięty. Naciśnij t jeżeli się zgadzasz:'.format(user.username, user.email))
                if user_delete == 't':
                    for key, value in user.__dict__.items():
                        print('{}: {}'.format(key, value), end='\n')
                    user.delete(cursor)
                    print('R.I.P')
                else:
                    print('Nadal żyw')

    elif options.list:
        users_all = User().load_all_users(cursor)
        for user in users_all:
            for key, value in user.__dict__.items():
                if key != '_User__hashed_password':
                    key = 'User Id' if key == '_User__id' else key
                    print('{}: {}'.format(key, value), end='\n')
            print('\n')

    else:

        print('Podaj parametr -h lub --help by zobaczyć możliwe parametry')

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    scenario(set_options())