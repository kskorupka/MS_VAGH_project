from flask import Blueprint, render_template, request, flash
from website.auxiliary_functions import contains_a_number

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", bool=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        if len(email) < 4 or email.find("@") == -1:
            flash('Niepoprawny email', category='error')
        elif len(firstName) < 3:
            flash('Imię powinno być dłuższe niż 1 litera', category='error')
        elif contains_a_number(firstName) == True:
            flash('Imię nie powinno zawierać liczb', category='error')
        elif password1 != password2:
            flash('Hasła nie są takie same', category='error')
        elif len(password1) < 8 or contains_a_number(password1) == False:
            flash('Hasło powinno składać się z 8 znaków oraz zawierać co najmniej jedną liczbę', category='error')
        else:
            flash('Konto zostało utworzone poprawnie', category='success')
            # add user to a database

    return render_template("sign_up.html")

