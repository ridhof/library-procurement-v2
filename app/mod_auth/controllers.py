"""
Auth Module's Controllers
"""
from flask import Blueprint, flash, render_template, request

from app.mod_auth.forms import LoginForm

from common import code

MOD_AUTH = Blueprint('auth', __name__, url_prefix='/')


@MOD_AUTH.route('', methods=['GET', 'POST'])
def login():
    """
    Return a HTML of Landing Page.
    """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        flash("Data berhasil masuk", code.FLASH_SUCCESS)
    return render_template("auth/login.html", form=form)
