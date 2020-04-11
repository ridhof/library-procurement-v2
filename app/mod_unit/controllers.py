"""
Unit Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_unit.forms import UnitForm
from app.mod_unit.models import Unit

from common import code, flash_code

MOD_UNIT = Blueprint('unit', __name__, url_prefix='/unit')

@MOD_UNIT.route('', methods=['GET'])
def table():
    """
    Return Unit Table Page
    """
    units = Unit.query.all()
    return render_template("unit/table.html", units=units)

@MOD_UNIT.route('/create', methods=['GET', 'POST'])
def create():
    """
    Return Create Page
    """
    form = UnitForm(request.form)
    if form.validate_on_submit():
        unit = Unit(
            f"{form.kode_fakultas.data}{form.kode_jurusan.data}",
            form.nama_unit.data,
            form.gedung.data,
            form.lantai.data,
            form.ruangan.data
        )
        error = unit.insert()
        if error:
            flash("Terjadi kesalahan", flash_code.DANGER)
        else:
            flash("Data berhasil disimpan", flash_code.SUCCESS)
            return redirect(url_for('unit.create'))
    form = UnitForm()
    return render_template("unit/form.html", form=form)
