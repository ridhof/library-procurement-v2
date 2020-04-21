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

@MOD_MATAKULIAH.route('/<matakuliah_id>/<matakuliah_kode>/ubah', methods=['GET', 'POST'])
def update(matakuliah_id, matakuliah_kode):
    """
    Return Update Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    matakuliah = Matakuliah.get_by_kode(matakuliah_id, matakuliah_kode)
    if matakuliah is None:
        flash(f"Terjadi kesalahan, Matakuliah dengan kode { matakuliah_kode } tidak dapat ditemukan", flash_code.WARNING)
        return redirect(url_for('matakuliah.table'))
    
    form = MatakuliahForm(request.form)
    if form.validate_on_submit():
        if matakuliah.kode != form.kode.data:
            if Matakuliah.query.filter_by(kode=form.kode.data, is_delete=0).first() is not None:
                flash(f"Matakuliah dengan kode { new_kode } sudah digunakan", flash_code.WARNING)
                form = MatakuliahForm(
                    data={
                        'matakuliah_id': matakuliah_id,
                        'kode': form.kode.data,
                        'nama': form.nama.data,
                        'sks': form.sks.data,
                        'deskripsi_singkat': form.deskripsi_singkat.data,
                        'standar_kompetensi': form.standar_kompetensi.data,
                        'tahun_ajaran': form.tahun_ajaran.data,
                        'kurikulum': form.kurikulum.data
                    }
                )
                return render_template("matakuliah/form.html", form=form, page_title="Ubah Matakuliah")
        
        matakuliah_update = Matakuliah.update(
            matakuliah_id=matakuliah_id,
            kode=form.kode.data,
            nama=form.nama.data,
            sks=form.sks.data,
            deskripsi_singkat=form.deskripsi_singkat.data,
            standar_kompetensi=form.standar_kompetensi.data,
            tahun_ajaran=form.tahun_ajaran.data,
            kurikulum=form.kurikulum.data
        )
        if matakuliah_update:
            flash(f"Matakuliah dengan Kode { matakuliah_kode } telah berhasil diubah", flash_code.SUCCESS)
            return redirect(url_for("matakuliah.update", matakuliah_id=matakuliah_id, matakuliah_kode=form.kode.data))
        
        flash(f"Terjadi kesalahan pada proses perubahan, data gagal disimpan", flash_code.DANGER)
        form = MatakuliahForm(
            data={
                'matakuliah_id': matakuliah_id,
                'kode': form.kode.data,
                'nama': form.nama.data,
                'sks': form.sks.data,
                'deskripsi_singkat': form.deskripsi_singkat.data,
                'standar_kompetensi': form.standar_kompetensi.data,
                'tahun_ajaran': form.tahun_ajaran.data,
                'kurikulum': form.kurikulum.data
            }
        )
    else:
        form = MatakuliahForm(
            data={
                'matakuliah_id': matakuliah_id,
                'kode': matakuliah_kode,
                'nama': matakuliah.nama,
                'sks': matakuliah.sks,
                'deskripsi_singkat': matakuliah.deskripsi_singkat,
                'standar_kompetensi': matakuliah.standar_kompetensi,
                'tahun_ajaran': matakuliah.get_kurikulum().split(' ')[0],
                'kurikulum': matakuliah.get_kurikulum().split(' ')[1].lower()
            }
        )
    return render_template("matakuliah/form.html", form=form, page_title="Ubah Matakuliah")

@MOD_MATAKULIAH.route('/<matakuliah_id>/<matakuliah_kode>/hapus', methods=['GET'])
def delete(matakuliah_id, matakuliah_kode):
    matakuliah_delete = Matakuliah.delete(matakuliah_id)
    if matakuliah_delete:
        flash(f"Matakuliah dengan kode { matakuliah_kode } telah berhasil dihapus", flash_code.SUCCESS)
        return redirect(url_for("matakuliah.table"))
    else:
        flash(f"Terjadi kesalahan, matakuliah dengan kode { matakuliah_kode } gagal dihapus", flash_code.DANGER)
        return redirect(url_for("matakuliah.update", matakuliah_id=matakuliah_id, matakuliah_kode=matakuliah_kode))
