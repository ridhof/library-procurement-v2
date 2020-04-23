"""
Pengusulan Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField
from wtforms.validators import Required


class PengusulanBaruForm(FlaskForm):
    """
    Form to create Pengusulan
    """
    pengusul_id = HiddenField("IdPengusul")

    pengarang = TextField("Pengarang", [Required()])
    judul = TextField("Judul", [Required()])
