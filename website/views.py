from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    :return: html template of home
    This function moves current_user to home's part.
    """
    return render_template("home.html", user=current_user)

