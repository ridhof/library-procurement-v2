"""
Unit Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField

from wtforms.validators import Required


class UnitForm(FlaskForm):
    """
    Forms to Create/Update Unit
    """
    unit_id = HiddenField("IdUnit")
    kode_fakultas = TextField('KodeFakultas', [Required()])
    kode_jurusan = TextField('KodeJurusan', [Required()])
    nama_unit = TextField('NamaUnit', [Required()])
    gedung = TextField('NamaGedung', [Required()])
    lantai = TextField('Lantai', [Required()])
    ruangan = TextField('Ruangan', [Required()])
