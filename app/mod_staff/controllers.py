"""
Staff Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_staff.forms import PasswordForm, StaffForm

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
    if user.is_superadmin:
        staffs = Staff.get_all()
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
        unit_id = user.unit_id
        if unit_id is None or unit_id == '':
            unit_id = 99

        staff = Staff(
            npk=form.npk.data,
            password="secret",
            nama=form.nama.data,
            unit_id=unit_id,
            is_kalab=0,
            is_kajur=0,
            perpus_role=perpus_code.ANGGOTA
        )

        if user.is_superadmin():
            staff.perpus_role = form.perpus_role.data
            staff.unit_id = form.unit_id.data
        elif user.is_pustakawan():
            staff.perpus_role = form.perpus_role.data

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

@MOD_STAFF.route('/<staff_id>/ubah', methods=['GET', 'POST'])
def update(staff_id):
    """
    Return Update Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    staff = Staff.find(staff_id)
    if staff is None:
        flash(f"Terjadi kesalahan, Staff dengan ID { staff_id } tidak dapat ditemukan", flash_code.WARNING)
        return redirect(url_for('staff.table'))

    form = StaffForm(request.form)
    if form.validate_on_submit():
        if staff.npk != form.npk.data:
            if Staff.query.filter_by(npk=form.npk.data, is_delete=0).first() is not None:
                flash(f"Terjadi kesalahan, Staff dengan NPK { form.npk.data } sudah digunakan", flash_code.WARNING)
                form_data = {
                    'staff_id': form.staff_id.data,
                    'npk': form.npk.data,
                    'nama': form.nama.data,
                    'role': form.role.data
                }
                if user.is_pustakawan() or user.is_superadmin():
                    form_data['perpus_role'] = form.perpus_role.data
                if user.is_superadmin():
                    form_data['unit_id'] = form.unit_id.data
                form = StaffForm(data=form_data)
                return render_template(
                    "staff/form.html", 
                    form=form, 
                    page_title="Ubah Staff", 
                    user=user
                )

        unit_id = None
        perpus_role = None
        if user.is_pustakawan() or user.is_superadmin():
            perpus_role = form.perpus_role.data
        if user.is_superadmin():
            unit_id = form.unit_id.data

        staff_update = Staff.update(
            staff_id=staff_id,
            npk=form.npk.data,
            nama=form.nama.data,
            role=form.role.data,
            unit_id=unit_id,
            perpus_role=perpus_role
        )
        if staff_update:
            flash(f"Staff dengan ID { staff_id } telah berhasil diubah", flash_code.SUCCESS)
            return redirect(url_for("staff.update", staff_id=staff_id))

        flash(f"Terjadi kesalahan pada proses perubahan, data gagal disimpan", flash_code.DANGER)
        form_data = {
            'staff_id': form.staff_id.data,
            'npk': form.npk.data,
            'nama': form.nama.data,
            'role': form.role.data
        }
        if user.is_pustakawan() or user.is_superadmin():
            form_data['perpus_role'] = form.perpus_role.data
        if user.is_superadmin():
            form_data['unit_id'] = form.unit_id.data
        form = StaffForm(data=form_data)
    else:
        form = StaffForm(
            data=staff.get_form_data(user.is_superadmin(), user.is_pustakawan())
        )
    return render_template(
        "staff/form.html", 
        form=form, 
        page_title="Ubah Staff", 
        user=user
    )

@MOD_STAFF.route('/<staff_id>/hapus', methods=['GET'])
def delete(staff_id):
    staff_delete = Staff.delete(staff_id)
    if staff_delete:
        flash(f"Staff dengan ID { staff_delete } telah berhasil dihapus", flash_code.SUCCESS)
        return redirect(url_for("staff.table"))
    else:
        flash(f"Terjadi kesalahan, Staff dengan ID { staff_id } gagal dihapus", flash_code.DANGER)
        return redirect(url_for("staff.update", staff_id=staff_id))

@MOD_STAFF.route('/<staff_id>/ubah/password', methods=['GET', 'POST'])
def password(staff_id):
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    form = PasswordForm(request.form)
    if form.validate_on_submit():
        if form.password.data != form.repassword.data:
            flash(f"Password yang diberikan tidak sama, pastikan kedua password sama", flash_code.WARNING)
        else:
            staff = Staff.find(staff_id)
            if staff is not None:
                if staff.change_password(form.password.data):
                    flash(f"Password untuk Staff dengan ID { staff_id } berhasil diubah", flash_code.SUCCESS)
                else:
                    flash(f"Terjadi kesalahan saat menyimpan password Staff { staff_id }, perubahan gagal disimapn", flash_code.DANGER)
            else:
                flash(f"Staff dengan ID { staff_id } tidak dapat ditemukan, gagal mengubah password", flash_code.DANGER)
            
    return render_template("staff/password_form.html", form=form)
