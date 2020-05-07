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

@MOD_MAHASISWA.route('<mahasiswa_id>/<mahasiswa_nrp>/ubah', methods=['GET', 'POST'])
def update(mahasiswa_id, mahasiswa_nrp):
    """
    Return Update Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    mahasiswa = Mahasiswa.get_by_nrp(mahasiswa_nrp)
    if mahasiswa is None:
        flash(f"Terjadi kesalahan, Mahasiswa tidak dapat ditemukan", flash_code.WARNING)
        return redirect(url_for('mahasiswa.table'))
    
    form = MahasiswaForm(request.form)
    if form.validate_on_submit():
        if mahasiswa.nrp != form.nrp.data:
            if Mahasiswa.get_by_nrp(form.nrp.data) is not None:
                flash(f"NRP telah digunakan, gagal mengubah data", flash_code.WARNING)
                return render_template("mahasiswa/form.html", form=form, page_title="Ubah Mahasiswa")
        
        if Mahasiswa.update(form.mahasiswa_id.data, form.nrp.data, form.nama.data):
            flash(f"Mahasiswa berhasil diubah", flash_code.SUCCESS)
            return redirect(url_for('mahasiswa.update', mahasiswa_id=mahasiswa_id, mahasiswa_nrp=form.nrp.data))
        else:
            flash(f"Terjadi kesalahan, data gagal disimpan", flash_code.DANGER)
    else:
        form = MahasiswaForm(data={
            'mahasiswa_id': mahasiswa.id,
            'unit_id': mahasiswa.unit_id,
            'nrp': mahasiswa.nrp,
            'nama': mahasiswa.nama
        })
    return render_template("mahasiswa/form.html", form=form, page_title="Ubah Mahasiswa")

@MOD_MAHASISWA.route('<mahasiswa_id>/<mahasiswa_nrp>/hapus', methods=['GET'])
def delete(mahasiswa_id, mahasiswa_nrp):
    if Mahasiswa.delete(mahasiswa_id):
        flash(f"Mahasiswa dengan NRP { mahasiswa_nrp } telah berhasil dihapus", flash_code.SUCCESS)
        return redirect(url_for("mahasiswa.table"))
    else:
        flash(f"Terjadi kesalahan, mahasiswa dengan NRP { mahasiswa_nrp } gagal dihapus", flash_code.DANGER)
        return redirect(url_for("mahasiswa.update", mahasiswa_id=mahasiswa_id, mahasiswa_nrp=mahasiswa_nrp))
