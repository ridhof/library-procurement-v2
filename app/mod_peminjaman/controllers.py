"""
Peminjaman Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_peminjaman.models import Peminjaman
from app.mod_peminjaman.forms import PeminjamanForm

from common import flash_code, peminjaman_code

MOD_PEMINJAMAN = Blueprint('peminjaman', __name__, url_prefix='/peminjaman/')

@MOD_PEMINJAMAN.route('', methods=['GET'])
def table():
    """
    Return Peminjaman Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    peminjamans = Peminjaman.get_peminjaman()
    return render_template("peminjaman/table.html", peminjamans=peminjamans, user=user)

@MOD_PEMINJAMAN.route('baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = PeminjamanForm(request.form)
    if form.validate_on_submit():
        if Peminjaman.check_buku(reg_comp=form.buku_regcomp.data) is None:
            flash(f"Buku dengan REG.COMP { form.buku_regcomp.data } tidak dapat ditemukan", flash_code.WARNING)
            return render_template("peminjaman/form.html", form=form, page_title="Tambah Peminjaman Baru", peminjaman_code=peminjaman_code)

        if Peminjaman.check_pemustaka(kode_pemustaka=form.peminjam_kode.data) is False:
            flash(f"Pemustaka (Mahasiswa/Staff) dengan kode { form.peminjam_kode.data } tidak dapat ditemukan", flash_code.WARNING)
            return render_template("peminjaman/form.html", form=form, page_title="Tambah Peminjaman Baru", peminjaman_code=peminjaman_code)
        
        peminjam = Peminjaman(
            verified_by=form.verified_by.data,
            buku_regcomp=form.buku_regcomp.data,
            pemustaka_kode=form.peminjam_kode.data,
            tanggal_pinjam=form.tanggal_pinjam.data,
            tanggal_tenggat=form.tanggal_tenggat.data,
            status=form.status.data
        )
        if peminjam.insert():
            flash(f"Peminjaman berhasil ditambahkan", flash_code.SUCCESS)
            return redirect(url_for('peminjaman.create'))
        else:
            flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)
    form.verified_by.data = user.id
    return render_template("peminjaman/form.html", form=form, page_title="Tambah Peminjaman Baru", peminjaman_code=peminjaman_code)
