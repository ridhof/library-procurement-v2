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
    return render_template("pengusulan/table.html", pengusulans=pengusulans, pengusulan_code=pengusulan_code)

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
