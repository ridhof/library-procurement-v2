"""
Peminjaman Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_peminjaman.models import Peminjaman
from app.mod_peminjaman.forms import FileForm, PeminjamanForm, get_datetime

from common import flash_code, peminjaman_code

MOD_PEMINJAMAN = Blueprint('peminjaman', __name__, url_prefix='/peminjaman/')

@MOD_PEMINJAMAN.route('periode/', methods=['GET'])
def periode():
    """
    Return Periode Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    periodes = Peminjaman.get_periode()
    now = get_datetime().split('-')
    periode_sekarang = f"{now[0]}-{now[1]}"
    return render_template("peminjaman/periode.html", periodes=periodes, user=user, periode_sekarang=periode_sekarang)

@MOD_PEMINJAMAN.route('<periode>/', methods=['GET'])
def table(periode):
    """
    Return Peminjaman Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    peminjamans = Peminjaman.get_peminjaman(periode=periode)
    return render_template("peminjaman/table.html", peminjamans=peminjamans, user=user, is_pustakawan=user.is_pustakawan(), periode=periode)

@MOD_PEMINJAMAN.route('<periode>/baru', methods=['GET', 'POST'])
def create(periode):
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
            return redirect(url_for('peminjaman.create', periode=periode))
        else:
            flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)
    form.verified_by.data = user.id
    return render_template("peminjaman/form.html", form=form, page_title="Tambah Peminjaman Baru", peminjaman_code=peminjaman_code, periode=periode)

@MOD_PEMINJAMAN.route('<periode>/import', methods=['GET', 'POST'])
def import_excel(periode):
    """
    Return Import Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    
    form = FileForm()
    if form.validate_on_submit():
        file_type = form.file_transaksi.data.filename.split('.')[1]
        if file_type == 'xlsx' or file_type == 'xls':
            filename = form.file_transaksi.data.filename
            path = './app/static/files/uploads/' + filename
            form.file_transaksi.data.save(path)
            sheet_index = 0
            
            if Peminjaman.import_excel(path, sheet_index):
                flash(f"File berhasil ditambahkan", flash_code.SUCCESS)
            else:
                flash(f"Proses import data gagal", flash_code.DANGER)
        else:
            flash(f"File yang diupload dimohon menggunakan format .xls ataupun .xlsx", flash_code.WARNING)
    return render_template("peminjaman/file-form.html", form=form, page_title="Impor Data Peminjaman", periode=periode)

@MOD_PEMINJAMAN.route('<periode>/<peminjaman_id>/hapus', methods=['GET'])
def delete(periode, peminjaman_id):
    if Peminjaman.delete(peminjaman_id):
        flash(f"Peminjaman telah berhasil dihapus", flash_code.SUCCESS)
    else:
        flash(f"Terjadi kesalahan, gagal menghapus peminjaman", flash_code.DANGER)
    return redirect(url_for("peminjaman.table", periode=periode))

@MOD_PEMINJAMAN.route('store', methods=['POST'])
def store():
    """
    Store Peminjaman
    """
    if request.method == 'POST':
        reg_comp = request.form['reg._comp']
        judul = request.form['judul_pustaka']
        anggota = request.form['id_anggota']
        tanggal_pinjam = request.form['tanggal_pinjam']
        tanggal_tenggat = request.form['tanggal_tenggat']
        status = request.form['status']
        petugas = request.form['petugas']
        
        status = status.lower()
        if status == peminjaman_code.KEMBALI or status == peminjaman_code.PERPANJANG or status == peminjaman_code.PINJAM:
            if Peminjaman.store_peminjaman(reg_comp, judul, anggota, tanggal_pinjam, tanggal_tenggat, status, petugas):
                return f"Berhasil menambahkan data ke Background Job"
        else:
            return f"Status peminjaman tidak dikenali, gagal menambahkan data"
    return f"Gagal menambah data"
