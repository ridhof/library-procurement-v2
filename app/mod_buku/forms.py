"""
Buku Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextField
from wtforms.validators import Required


class BukuForm(FlaskForm):
    """
    Form to create or update Buku
    """
    buku_id = HiddenField("IdBuku")
    reg_comp = TextField("RegComp", [Required()])
    judul = TextField("Judul", [Required()])
