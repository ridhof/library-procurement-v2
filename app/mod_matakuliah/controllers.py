"""
Matakuliah Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_matakuliah.forms import MatakuliahForm
from app.mod_matakuliah.models import Matakuliah

from common import flash_code

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

@MOD_MATAKULIAH.route('/baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = MatakuliahForm(request.form)
    if form.validate_on_submit():

        matakuliah = Matakuliah(
            kode=form.kode.data,
            nama=form.nama.data,
            sks=form.sks.data,
            deskripsi_singkat=form.deskripsi_singkat.data,
            standar_kompetensi=form.standar_kompetensi.data,
            unit_id=user.unit_id,
            kurikulum=f"{form.tahun_ajaran.data}-{form.kurikulum.data}"
        )

        if Matakuliah.query.filter_by(kode=matakuliah.kode, is_delete=0).first() is not None:
            flash(f"Gagal menambahkan data, Matakuliah dengan kode { matakuliah.kode } sudah digunakan", flash_code.DANGER)
        else:
            if matakuliah.insert():
                flash(f"Matakuliah dengan kode { matakuliah.kode } berhasil disimpan", flash_code.SUCCESS)
                return redirect(url_for('matakuliah.create'))
            else:
                flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)
            
    return render_template("matakuliah/form.html", form=form, page_title="Buat Matakuliah Baru")
