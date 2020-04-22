"""
RPS Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField
from wtforms.validators import Required


class RpsForm(FlaskForm):
    """
    Form to create or update RPS
    """
    rps_id = HiddenField("IdRps")
    matakuliah_id = HiddenField("IdMatakuliah")

    kompetensi_dasar = TextAreaField("KompetensiDasar", [Required()])
    indikator_capaian = TextAreaField("IndikatorCapaian", [Required()])
    materi = TextAreaField("Materi", [Required()])
