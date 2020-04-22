"""
RPS Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_rps.models import Rps

from common import flash_code

MOD_RPS = Blueprint('rps', __name__, url_prefix='/rps/')


@MOD_RPS.route('<matakuliah_id>/<matakuliah_kode>/data', methods=['GET'])
def table(matakuliah_id, matakuliah_kode):
    """
    Return RPS Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    rpses = Rps.get_by_matakuliah_id(matakuliah_id)
    return render_template("rps/table.html", rpses=rpses, matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode)
