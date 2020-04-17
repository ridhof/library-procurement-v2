"""
Auth Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.mod_auth.forms import LoginForm
from app.mod_auth.models import Staff

from common import code, flash_code

MOD_AUTH = Blueprint('auth', __name__, url_prefix='/')


@MOD_AUTH.route('', methods=['GET', 'POST'])
def login():
    """
    Return a HTML of Landing Page.
    """
    if session.get('user_id') is not None:
        print(session.get('user_name'))
        flash("Anda sudah login", flash_code.INFO)
        return redirect(url_for('dashboard.dashboard'))
        
    form = LoginForm(request.form)
    if form.validate_on_submit():
        result = Staff.login(form.npk.data, form.password.data)
        if result["status"] == code.OK:
            staff = result["staff"]
            session['user_id'] = staff.id
            session['user_name'] = staff.nama
            flash("Anda berhasil masuk", flash_code.SUCCESS)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("NPK/Password anda tidak sesuai", flash_code.DANGER)
        # Register Purposes
        # staff = Staff(form.npk.data, form.password.data)
        # error = staff.insert()
        # if error:
        #     flash("Terjadi kesalahan", flash_code.DANGER)
        # else:
        #     flash("Data berhasil masuk", flash_code.SUCCESS)
        #     form = LoginForm()
    return render_template("auth/login.html", form=form)

@MOD_AUTH.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Berhasil logout', 'info')
    return redirect(url_for('auth.login'))

@MOD_AUTH.route('/password', methods=['GET'])
def password():
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    return redirect(url_for('staff.password', staff_id=user.id, staff_npk=user.npk))
