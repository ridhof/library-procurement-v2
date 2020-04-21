"""
Referensi Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_referensi.models import Referensi
from app.mod_referensi.forms import ReferensiForm

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
    return render_template("referensi/table.html", referensis=referensis, matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode)

@MOD_REFERENSI.route('<matakuliah_id>/<matakuliah_kode>/baru', methods=['GET', 'POST'])
def create(matakuliah_id, matakuliah_kode):
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = ReferensiForm(request.form)
    if form.validate_on_submit():
        referensi = Referensi(
            pengarang=form.pengarang.data,
            judul=form.judul.data,
            keterangan=form.keterangan.data,
            matakuliah_id=form.matakuliah_id.data
        )

        if referensi.insert():
            flash(f"Referensi berhasil disimpan", flash_code.SUCCESS)
            return redirect(url_for('referensi.create', matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode))
        else:
            flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)

    form.matakuliah_id.data = matakuliah_id
    return render_template("referensi/form.html", form=form, page_title="Buat Referensi Baru", matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode)
