"""
Mahasiswa Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_mahasiswa.models import Mahasiswa
from app.mod_mahasiswa.forms import MahasiswaForm

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

@MOD_MAHASISWA.route('baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = MahasiswaForm(request.form)
    if form.validate_on_submit():
        mahasiswa = Mahasiswa(
            unit_id=user.unit_id,
            nrp=form.nrp.data,
            nama=form.nama.data
        )

        if Mahasiswa.nrp_available(mahasiswa.nrp) is not None:
            flash(f"Gagal menambahkan data, NRP sudah digunakan", flash_code.DANGER)
        else:
            if mahasiswa.insert():
                flash(f"Mahasiswa berhasil disimpan", flash_code.SUCCESS)
                return redirect(url_for('mahasiswa.create'))
            else:
                flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)
                
    return render_template("mahasiswa/form.html", form=form, page_title="Tambah Mahasiswa Baru")
