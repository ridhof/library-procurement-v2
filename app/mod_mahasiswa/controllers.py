"""
Mahasiswa Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_mahasiswa.models import Mahasiswa

from common import flash_code

MOD_MAHASISWA = Blueprint('mahasiswa', __name__, url_prefix='/mahasiswa/')


@MOD_MAHASISWA.route('', methods=['GET'])
def table():
    """
    Return Mahasiswa Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    mahasiswas = Mahasiswa.get_by_unit(user.unit_id)
    return render_template("mahasiswa/table.html", mahasiswas=mahasiswas, user=user)
