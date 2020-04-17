"""
Matakuliah Module's Controllers
"""
from flask import Blueprint, redirect, render_template, url_for

from app.mod_auth.models import Staff
from app.mod_matakuliah.models import Matakuliah

MOD_MATAKULIAH = Blueprint('matakuliah', __name__, url_prefix='/matakuliah/')


@MOD_MATAKULIAH.route('', methods=['GET'])
def table():
    """
    Return Matakuliah Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    matakuliahs = Matakuliah.get_by_unit(user.unit_id)
    return render_template("matakuliah/table.html", matakuliahs=matakuliahs, user=user)
