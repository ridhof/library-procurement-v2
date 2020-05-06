"""
Mahasiswa Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField
from wtforms.validators import Required


class MahasiswaForm(FlaskForm):
    """
    Form to create or update Mahasiswa
    """
    mahasiswa_id = HiddenField("IdMahasiswa")
    nrp = TextField("NRP", [Required()])
    nama = TextField("Nama", [Required()])
