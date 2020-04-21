"""
Referensi Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_referensi.models import Referensi

from common import flash_code

MOD_REFERENSI = Blueprint('referensi', __name__, url_prefix='/referensi/')


@MOD_REFERENSI.route('<matakuliah_id>/<matakuliah_kode>/data', methods=['GET'])
def table(matakuliah_id, matakuliah_kode):
    """
    Return Referensi Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    referensis = Referensi.get_by_matakuliah_id(matakuliah_id)
    return render_template("referensi/table.html", referensis=referensis)
