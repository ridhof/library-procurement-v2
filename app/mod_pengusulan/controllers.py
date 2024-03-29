"""
Pengusulan Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_pengusulan.models import Pengusulan, Relevansi
from app.mod_pengusulan.forms import PengusulanBaruForm

from common import flash_code, pengusulan_code


MOD_PENGUSULAN = Blueprint('pengusulan', __name__, url_prefix='/pengusulan/')


@MOD_PENGUSULAN.route('', methods=['GET'])
def table():
    """
    Return Pengusulan Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    pengusulans = Pengusulan.get_by_staff(user.id)
    ranks = Pengusulan.calculate_averages(pengusulans)
    return render_template("pengusulan/table.html", pengusulans=pengusulans, ranks=ranks, pengusulan_code=pengusulan_code, user=user)

@MOD_PENGUSULAN.route('analisa/', methods=['GET'])
def analyze():
    """
    Return Pengusulan Table Page From Other Unit
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    pengusulans = Pengusulan.get_all()
    ranks = Pengusulan.calculate_averages(pengusulans)
    return render_template("pengusulan/analisa-table.html", pengusulans=pengusulans, ranks=ranks, pengusulan_code=pengusulan_code, status=pengusulan_code.DIUSULKAN)

@MOD_PENGUSULAN.route('analisa/semua', methods=['GET'])
def analyze_all():
    """
    Return All Pengusulan Table Page From Other Unit
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    pengusulans = Pengusulan.get_all(status=None)
    ranks = Pengusulan.calculate_averages(pengusulans)
    return render_template("pengusulan/analisa-table.html", pengusulans=pengusulans, ranks=ranks, pengusulan_code=pengusulan_code, status=None)

@MOD_PENGUSULAN.route('kelola/', methods=['GET'])
def manage():
    """
    Return Pengusulan Table Manage Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    
    if user.get_unit_role() == 'staff':
        return redirect(url_for('pengusulan.table'))

    pengusulans = Pengusulan.get_by_unit(user.unit_id)
    ranks = Pengusulan.calculate_averages(pengusulans)
    return render_template("pengusulan/kelola-table.html", ranks=ranks, pengusulans=pengusulans, pengusulan_code=pengusulan_code, status=pengusulan_code.DIUSULKAN)

@MOD_PENGUSULAN.route('kelola/semua', methods=['GET'])
def manage_all():
    """
    Return All Pengusulan Table Manage Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    if user.get_unit_role() == 'staff':
        return redirect(url_for('pengusulan.table'))

    pengusulans = Pengusulan.get_by_unit(
        unit_id=user.unit_id,
        status=None
    )
    ranks = Pengusulan.calculate_averages(pengusulans)
    return render_template("pengusulan/kelola-table.html", pengusulans=pengusulans, ranks=ranks, pengusulan_code=pengusulan_code, status=None)

@MOD_PENGUSULAN.route('<pengusulan_id>/relevansi')
def relevansi(pengusulan_id):
    """
    Return All Relevansi of Pengusulan
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    relevansis = Relevansi.get_by_pengusulan(pengusulan_id)
    return render_template("pengusulan/relevansi-table.html", relevansis=relevansis)

@MOD_PENGUSULAN.route('kelola/<pengusulan_id>/<status>')
def approve(pengusulan_id, status):
    """
    Run Pengusulan Approval Functions
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    if user.get_unit_role() == 'staff':
        flash(f"Anda tidak memiliki akses untuk melakukan approval pengusulan", flash_code.WARNING)
        return redirect(url_for('pengusulan.table'))

    pengusulan_approve = Pengusulan.approve(
        pengusulan_id=pengusulan_id,
        status=status,
        petugas_id=user.id
    )
    if pengusulan_approve:
        flash(f"Status Pengusulan Buku telah berhasil diperbarui", flash_code.SUCCESS)
    else:
        flash(f"Status Pengusulan Buku gagal diperbarui", flash_code.DANGER)
    return redirect(url_for('pengusulan.manage'))

@MOD_PENGUSULAN.route('baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = PengusulanBaruForm(request.form)
    form.set_matakuliah(user.unit_id)
    if form.is_submitted():
        pengusulan = Pengusulan(
            pengarang=form.pengarang.data,
            judul=form.judul.data,
            pengusul_id=form.pengusul_id.data
        )

        if pengusulan.insert(form.matakuliah.data):
            flash(f"Pengusulan berhasil disimpan", flash_code.SUCCESS)
            return redirect(url_for('pengusulan.create'))
        else:
            flash(f"Gagal menambahkan data, terjadi kesalahan", flash_code.DANGER)

    form.pengusul_id.data = user.id
    return render_template("pengusulan/form/baru.html", form=form, page_title="Buat Pengusulan Baru")

@MOD_PENGUSULAN.route('<pengusulan_id>/hapus', methods=['GET'])
def delete(pengusulan_id):
    pengusulan_delete = Pengusulan.delete(pengusulan_id)
    if pengusulan_delete:
        flash(f"Pengusulan telah dibatalkan", flash_code.SUCCESS)
    else:
        flash(f"Terjadi kesalahan, Pengusulan gagal dibatalkan", flash_code.DANGER)
    return redirect(url_for("pengusulan.table"))

@MOD_PENGUSULAN.route('<pengusulan_id>/preprocess/simpan', methods=['POST'])
def store_preprocess(pengusulan_id):
    """
    Store Preprocessed Pengusulan
    """
    if request.method == 'POST':
        preprocessed_judul = request.form['preprocessed_judul']
        if Pengusulan.store_preprocessed(pengusulan_id, preprocessed_judul):
            pengusulan = Pengusulan.query.filter_by(id=pengusulan_id).first()
            if not pengusulan.calculate_similarity():
                print("gagal menyimpan")
            return f'Berhasil disimpan'
    return f'Gagal melakukan penyimpanan'

@MOD_PENGUSULAN.route('<relevansi_id>/score/simpan', methods=['POST'])
def store_score(relevansi_id):
    """
    Store Process Score
    """
    if request.method == 'POST':
        score = request.form['score']
        if Relevansi.store_score(relevansi_id, score):
            return f'Berhasil disimpan'
    return f'Gagal melakukan penyimpanan'
