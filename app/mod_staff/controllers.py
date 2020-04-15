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
    
    user_role = 'karyawan'
    if user.is_kajur:
        user_role = 'kajur'
    elif user.is_kalab:
        user_role = 'kalab'

    staffs = Staff.get_by_unit(user.unit_id)
    return render_template("staff/table.html", staffs=staffs, user_role=user_role, user=user)

@MOD_STAFF.route('/baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    if not (user.is_kajur or user.is_kalab or user.perpus_role == 'dev'):
        flash("Akun anda tidak dapat mengakses atau melakukan hal tersebut", flash_code.WARNING)
        return redirect(url_for('staff.table'))

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
    return render_template("staff/form.html", form=form, page_title="Tambah Staff Baru", user=user)

@MOD_STAFF.route('/<staff_id>/<staff_npk>/ubah', methods=['GET', 'POST'])
def update(staff_id, staff_npk):
    """
    Return Update Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    staff = Staff.get_by_npk(staff_id, staff_npk)
    if staff is None:
        flash(f"Terjadi kesalahan, Staff dengan kode { staff_npk } tidak dapat ditemukan", flash_code.WARNING)
        return redirect(url_for('staff.table'))

    form = StaffForm(request.form)
    if form.validate_on_submit():
        if staff.npk != form.npk.data:
            if Staff.query.filter_by(npk=form.npk.data, is_delete=0).first() is not None:
                flash(f"Terjadi kesalahan, Staff dengan NPK { form.npk.data } sudah digunakan", flash_code.WARNING)
                form = StaffForm(
                    data={
                        'staff_id': form.staff_id.data,
                        'npk': form.npk.data,
                        'nama': form.nama.data,
                        'role': form.role.data
                    }
                )
                return render_template(
                    "staff/form.html", 
                    form=form, 
                    page_title="Ubah Staff", 
                    user=user
                )


        staff_update = Staff.update(
            staff_id=staff_id,
            npk=form.npk.data,
            nama=form.nama.data,
            role=form.role.data
        )
        if staff_update:
            flash(f"Staff dengan NPK { staff_npk } telah berhasil diubah", flash_code.SUCCESS)
            return redirect(url_for("staff.update", staff_id=staff_id, staff_npk=form.npk.data))

        flash(f"Terjadi kesalahan pada proses perubahan, data gagal disimpan", flash_code.DANGER)
        form = StaffForm(
            data={
                'staff_id': form.staff_id.data,
                'npk': form.npk.data,
                'nama': form.nama.data,
                'role': form.role.data
            }
        )
    else:
        form = StaffForm(
            data={
                'staff_id': staff_id,
                'npk': staff.npk,
                'nama': staff.nama,
                'role': staff.get_unit_role()
            }
        )
    return render_template(
        "staff/form.html", 
        form=form, 
        page_title="Ubah Staff", 
        user=user
    )
