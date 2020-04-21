"""
Referensi Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField
from wtforms.validators import Required


class ReferensiForm(FlaskForm):
    """
    Form to create or update Referensi
    """
    referensi_id = HiddenField("IdReferensi")
    matakuliah_id = HiddenField("IdMatakuliah")

    pengarang = TextField("Pengarang", [Required()])
    judul = TextField("Judul", [Required()])
    keterangan = TextField("Keterangan", [Required()])
