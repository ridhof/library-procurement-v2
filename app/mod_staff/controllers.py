"""
Staff Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_staff.forms import StaffForm

from common import flash_code, perpus_code

MOD_STAFF = Blueprint('staff', __name__, url_prefix='/staff/')

@MOD_STAFF.route('', methods=['GET'])
def table():
    """
    Return Staff Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    staffs = Staff.get_all()
    return render_template("staff/table.html", staffs=staffs, user_role=user.perpus_role)

@MOD_STAFF.route('/baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = StaffForm(request.form)
    if form.validate_on_submit():
        staff = Staff(
            npk=form.npk.data,
            password="secret",
            nama=form.nama.data,
            unit_id=2,
            is_kalab=0,
            is_kajur=0,
            perpus_role=perpus_code.ANGGOTA
        )

        if form.role.data == 'kajur':
            staff.is_kajur = 1
        elif form.role.data == 'kalab':
            staff.is_kalab = 1

        if Staff.query.filter_by(npk=staff.npk, is_delete=0).first() is not None:
            flash(f"Tidak dapat menyimpan data, NPK { staff.npk } sudah digunakan", flash_code.DANGER)
        else:
            if staff.insert():
                flash(f"Staff dengan NPK { staff.npk } telah berhasil disimpan", flash_code.SUCCESS)
                return redirect(url_for('staff.create'))
            else:
                flash("Terjadi kesalahan, gagal menyimpan data", flash_code.DANGER)
    return render_template("staff/form.html", form=form, page_title="Tambah Staff Baru")
