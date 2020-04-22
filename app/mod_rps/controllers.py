"""
RPS Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_rps.models import Rps
from app.mod_rps.forms import RpsForm

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

@MOD_RPS.route('<matakuliah_id>/<matakuliah_kode>/baru', methods=['GET', 'POST'])
def create(matakuliah_id, matakuliah_kode):
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = RpsForm(request.form)
    if form.validate_on_submit():
        rps = Rps(
            kompetensi_dasar=form.kompetensi_dasar.data,
            indikator_capaian=form.indikator_capaian.data,
            materi=form.materi.data,
            matakuliah_id=form.matakuliah_id.data
        )

        if rps.insert():
            flash(f"RPS berhasil disimpan", flash_code.SUCCESS)
            return redirect(url_for('rps.create', matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode))
        else:
            flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)

    form.matakuliah_id.data = matakuliah_id
    return render_template("rps/form.html", form=form, page_title="Buat RPS Baru", matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode)
