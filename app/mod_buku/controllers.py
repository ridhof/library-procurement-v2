"""
Buku Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_buku.models import Buku, Dewey
from app.mod_buku.forms import BukuForm

from common import flash_code

MOD_BUKU = Blueprint('buku', __name__, url_prefix='/buku/')

@MOD_BUKU.route('', methods=['GET'])
def table():
    """
    Return Buku Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    bukus = Buku.get_buku()
    return render_template("buku/table.html", bukus=bukus, user=user)

@MOD_BUKU.route('baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    
    form = BukuForm(request.form)
    if form.validate_on_submit():
        buku = Buku(
            reg_comp=form.reg_comp.data,
            judul=form.judul.data
        )
        if Buku.regcomp_available(buku.reg_comp) is not None:
            flash(f"Gagal menambahkan data, REG.COMP telah digunakan", flash_code.DANGER)
        else:
            if buku.insert():
                flash(f"Buku berhasil disimpan", flash_code.SUCCESS)
                return redirect(url_for('buku.create'))
            else:
                flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)
    
    return render_template("buku/form.html", form=form, page_title="Tambah Buku Buru")

@MOD_BUKU.route('<buku_id>/ubah', methods=['GET', 'POST'])
def update(buku_id):
    """
    Return Update Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    buku = Buku.get_buku(buku_id=buku_id)
    if buku is None:
        flash(f"Buku tidak dapat ditemukan", flash_code.WARNING)
        return redirect(url_for('buku.table'))
    
    form = BukuForm(request.form)
    if form.validate_on_submit():
        if buku.reg_comp != form.reg_comp.data:
            if Buku.regcomp_available(form.reg_comp.data) is not None:
                flash(f"REG.COMP telah digunakan, gagal mengubah data", flash_code.WARNING)
                return render_template("buku/form.html", form=form, page_title="Ubah Buku")

        if Buku.update(buku_id, form.reg_comp.data, form.judul.data):
            flash(f"Buku berhasil diubah", flash_code.SUCCESS)
            return redirect(url_for('buku.update', buku_id=buku_id))
        else:
            flash(f"Terjadi kesalahan, data gagal disimpan", flash_code.DANGER)
    else:
        form = BukuForm(data={
            'buku_id': buku.id,
            'reg_comp': buku.reg_comp,
            'judul': buku.judul
        })
    return render_template("buku/form.html", form=form, page_title="Ubah Buku")

@MOD_BUKU.route('<buku_id>/hapus', methods=['GET'])
def delete(buku_id):
    if Buku.delete(buku_id):
        flash(f"Buku telah berhasil dihapus", flash_code.SUCCESS)
        return redirect(url_for("buku.table"))
    else:
        flash(f"Terjadi kesalahan, buku dengan ID { buku_id } gagal dihapus", flash_code.DANGER)
        return redirect(url_for("buku.update", buku_id=buku_id))

@MOD_BUKU.route('<buku_id>/preprocess/simpan', methods=['POST'])
def store_preprocess(buku_id):
    """
    Store Preprocessed Judul
    """
    if request.method == 'POST':
        preprocessed_judul = request.form['preprocessed_judul']
        if Buku.store_preprocessed(buku_id, preprocessed_judul):
            return f'Berhasil disimpan'
    return f'Gagal melakukan penyimpanan'

@MOD_BUKU.route('dewey/baru', methods=['POST'])
def store_dewey():
    """
    Store Dewey
    """
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        preprocessed_nama = request.form['preprocessed_nama']

        dewey = Dewey(kode, nama, preprocessed_nama=preprocessed_nama)
        if dewey.insert():
            return f"Berhasil melakukan penyimpanan data"
    return f"Gagal melakukan penyimpanan data"


