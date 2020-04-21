"""
Matakuliah Module's Forms
"""
import datetime
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, TextAreaField, TextField
from wtforms.validators import Required

def get_tahun_ajaran():
    now = datetime.datetime.now()
    tahun = now.year + 3
    list_tahun_ajaran = []
    for i in range(2016, tahun):
        list_tahun_ajaran.append(
            (f"{ i }/{ i + 1 }", f"{ i }/{ i + 1 }")
        )
    return list_tahun_ajaran

def get_current():
    now = datetime.datetime.now()
    tahun = now.year
    return f"{tahun}/{tahun + 1}"

class MatakuliahForm(FlaskForm):
    """
    Form to create or update Matakuliah
    """
    matakuliah_id = HiddenField("IdMatakuliah")
    kode = TextField("Kode", [Required()])
    nama = TextField("Nama", [Required()])
    sks = TextField("SKS", [Required()])
    deskripsi_singkat = TextAreaField("DeskripsiSingkat", [Required()])
    standar_kompetensi = TextAreaField("StandarKompetensi", [Required()])
    tahun_ajaran = SelectField(
        'Role',
        choices=get_tahun_ajaran(),
        validators=[Required()],
        default=get_current()
    )
    kurikulum = SelectField(
        'Role',
        choices=[
            ('ganjil', 'Ganjil'),
            ('genap', 'Genap')
        ],
        validators=[Required()],
        default='ganjil'
    )
