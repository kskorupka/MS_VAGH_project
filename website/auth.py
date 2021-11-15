from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

#TODO time:   58:42
@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html", bool=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template("sign_up.html")
