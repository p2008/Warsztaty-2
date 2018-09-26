import argparse
import re
from controllers.connect_db import create_connection
from models.user import User
from controllers.hash_password import check_password
from psycopg2 import IntegrityError


def validate_email():
    pattern = re.compile(r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]{1,})*\.([a-zA-Z]{2,}){1}$')
    email = input('Podaj nowy email:\n')
    match = pattern.fullmatch(email)

    while not match:
        print("Podany e-mail jest niepoprawny")
        email = input('Podaj nowy email:\n')
        match = pattern.fullmatch(email)

    return match.string


def validate_password(new_pass):
    pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    match = pattern.fullmatch(new_pass)

    while not match:
        print("Hasło powinno skladac sie z 8 znakow w tym co najmniej jedna litera, jedna liczba i jeden znak specjalny: @$!%*#?&")
        new_pass = input('Podaj hasło:\n')
        match = pattern.fullmatch(new_pass)

    return match.string


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest='username', help="User login")
    parser.add_argument("-p", "--password", dest='password', help="User password")
    parser.add_argument("-n", "--new-pass", dest='newpass', help="User new password")
    parser.add_argument("-l", "--list", dest='list', action='store_true', default=False, help="List all users")
    parser.add_argument("-d", "--delete", dest='delete', action='store_true', help="Delete user")
    parser.add_argument("-e", "--edit", dest='edit', action='store_true', help="Change user login")

    options, unknown = parser.parse_known_args()
    return options


def scenario(options):
    cnx = create_connection('exam2')
    cursor = cnx.cursor()
    user_obj = User()
    user = None
    password = None
    newpass = None

    if options.username and options.password and not options.edit and not options.delete and not options.newpass:
        if user_obj.load_user_by_name(cursor, options.username) is not None:
            password = user_obj.load_user_by_name(cursor, options.username).hashed_password
            if check_password(options.password, password):
                email = user_obj.load_user_by_name(cursor, options.username).email

                if email is not None:
                    print('Użytkownik o email: {} już istnieje'.format(email))
            else:
                print('Podane hasło jest błędne')
        else:
            try:
                user_obj.username = options.username
                user_obj.email = validate_email()
                password_new = validate_password(options.password)
                user_obj.set_password(password_new, salt=None)
                user_obj.save_to_db(cursor)
                print('Użytkownik: {} i email: {} został utworzony'.format(user_obj.username, user_obj.email))
            except IntegrityError as e:
                print(e, "Użytkownik lub e-mail są już w bazie")

            user_obj.save_to_db(cursor)

    elif options.username and options.password and options.edit and options.newpass and not options.delete:
        user = user_obj.load_user_by_name(cursor, options.username)
        password = user.hashed_password
        newpass = validate_password(options.newpass)
        if check_password(options.password, password):
            if newpass is not None:
                password_new = validate_password(options.newpass)
                user_obj.set_password(password_new, salt=None)
                user.save_to_db(cursor)
                print('nowe hasło ustawione')
            else:
                print('Ustaw właściwe hasło w przełączniku -n')
        else:
            print('Hasło niepoprawne')

    elif options.username and options.password and options.delete and not options.edit and not options.newpass:
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

    elif options.list and not options.newpass:
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
