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
    return render_template("pengusulan/table.html", pengusulans=pengusulans, pengusulan_code=pengusulan_code, user=user)

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
    return render_template("pengusulan/kelola-table.html", pengusulans=pengusulans, pengusulan_code=pengusulan_code)

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
