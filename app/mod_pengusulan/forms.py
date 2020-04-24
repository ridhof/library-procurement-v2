"""
Pengusulan Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, TextField
from wtforms.validators import Required

from app.mod_matakuliah.models import Matakuliah

def get_matakuliah(unit_id):
    matakuliahs = Matakuliah.get_by_unit(unit_id)
    list_matakuliah = []
    for matakuliah in matakuliahs:
        list_matakuliah.append(
            (matakuliah.id, f"{ matakuliah.kode } - { matakuliah.nama }")
        )
    return list_matakuliah

class PengusulanBaruForm(FlaskForm):
    """
    Form to create Pengusulan
    """
    pengusul_id = HiddenField("IdPengusul")

    pengarang = TextField("Pengarang", [Required()])
    judul = TextField("Judul", [Required()])
    matakuliah = SelectMultipleField(
        "Matakuliah",
        choices=[],
        validators=[Required()]
    )

    def set_matakuliah(self, unit_id):
        self.matakuliah.choices = get_matakuliah(unit_id)
