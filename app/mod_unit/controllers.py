"""
Unit Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_unit.forms import UnitForm

from app.mod_auth.models import Staff
from app.mod_unit.models import Unit

from common import code, flash_code, perpus_code

MOD_UNIT = Blueprint('unit', __name__, url_prefix='/unit/')

@MOD_UNIT.route('', methods=['GET'])
def table():
    """
    Return Unit Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))
    allow_edit = False
    if user.is_kajur or user.is_kalab or user.perpus_role == perpus_code.DEV:
        allow_edit = True
    units = Unit.get_all()
    return render_template("unit/table.html", units=units, user_role=user.perpus_role, user_unit_id=user.unit_id, allow_edit=allow_edit)

@MOD_UNIT.route('/baru', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    if not user.is_role(perpus_code.DEV):
        return redirect(url_for('unit.table'))

    form = UnitForm(request.form)
    if form.validate_on_submit():
        unit = Unit(
            f"{form.kode_fakultas.data}{form.kode_jurusan.data}",
            form.nama_unit.data,
            form.gedung.data,
            form.lantai.data,
            form.ruangan.data
        )
        if Unit.query.filter_by(kode=unit.kode, is_delete=0).first() is not None:
            flash(f"Gagal menambahkan data, Unit dengan kode { unit.kode } sudah digunakan", flash_code.DANGER)
        else:
            if unit.insert():
                flash(f"Unit dengan kode { unit.kode } berhasil disimpan", flash_code.SUCCESS)
                return redirect(url_for('unit.create'))
            else:
                flash("Terjadi kesalahan", flash_code.DANGER)
    return render_template("unit/form.html", form=form, page_title="Buat Unit Baru")

@MOD_UNIT.route('/<unit_id>/<unit_kode>/ubah', methods=['GET', 'POST'])
def update(unit_id, unit_kode):
    """
    Return Update Page
    """
    user = Staff.is_login() 
    if user is None:
        return redirect(url_for('auth.login'))

    unit = Unit.get_by_kode(unit_id, unit_kode)
    if unit is None:
        flash(f"Terjadi kesalahan, Unit dengan kode { unit_kode } tidak dapat ditemukan.", flash_code.WARNING)
        return redirect(url_for('unit.table'))
    form = UnitForm(request.form)
    if form.validate_on_submit():
        new_kode = f"{form.kode_fakultas.data}{form.kode_jurusan.data}"

        if Unit.query.filter_by(kode=new_kode, is_delete=0).first() is None:
            unit_update = Unit.update(
                unit_id=form.unit_id.data, 
                kode_unit=new_kode,
                nama=form.nama_unit.data,
                gedung=form.gedung.data,
                lantai=form.lantai.data,
                ruangan=form.ruangan.data
            )
            if unit_update:
                flash(f"Unit dengan kode { unit_kode } telah berhasil diubah", flash_code.SUCCESS)
                return redirect(url_for("unit.update", unit_id=unit_id, unit_kode=new_kode))
        else:
            flash(f"Unit dengan kode { new_kode } sudah digunakan", flash_code.WARNING)
        
        flash(f"Terjadi kesalahan sehingga data gagal diubah", flash_code.DANGER)
        form = UnitForm(
            data={
                'unit_id': form.unit_id.data,
                'kode_fakultas': form.kode_fakultas.data,
                'kode_jurusan': form.kode_jurusan.data,
                'nama_unit': form.nama_unit.data,
                'gedung': form.gedung.data,
                'lantai': form.lantai.data,
                'ruangan': form.ruangan.data
            }
        )
    else:
        form = UnitForm(
            data={
                'unit_id': unit_id,
                'kode_fakultas': unit.kode[0],
                'kode_jurusan': unit.kode[1],
                'nama_unit': unit.nama,
                'gedung': unit.gedung,
                'lantai': unit.lantai,
                'ruangan': unit.ruangan
            }
        )
    return render_template("unit/form.html", form=form, page_title="Ubah Unit", user_role=user.perpus_role)

@MOD_UNIT.route('/<unit_id>/<kode_unit>hapus', methods=['GET'])
def delete(unit_id, kode_unit):
    unit_delete = Unit.delete(unit_id)
    if unit_delete:
        flash(f"Unit dengan kode { kode_unit } telah berhasil dihapus", flash_code.SUCCESS)
        return redirect(url_for("unit.table"))
    else:
        flash(f"Terjadi kesalahan, unit dengan kode { kode_unit } gagal dihapus", flash_code.DANGER)
        return redirect(url_for("unit.update", unit_id=unit_id, unit_kode=kode_unit))
