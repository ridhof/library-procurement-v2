"""
Staff Module's Controllers
"""
from flask import Blueprint, redirect, render_template, url_for

from app.mod_auth.models import Staff

MOD_STAFF = Blueprint('staff', __name__, url_prefix='/staff/')

@MOD_STAFF.route('', methods=['GET'])
def table():
    """
    Return Staff Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    staffs = Staff.get_all()
    return render_template("staff/table.html", staffs=staffs, user_role=user.perpus_role)
