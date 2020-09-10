"""
Peminjaman Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, TextField, FileField
from wtforms.validators import Required
from common import peminjaman_code
import datetime


def get_datetime():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d")

class FileForm(FlaskForm):
    """
    Form to import File
    """
    file_transaksi = FileField("FileTransaksi", [Required()])

class PeminjamanForm(FlaskForm):
    """
    Form to create Peminjaman
    """
    peminjaman_id = HiddenField("IdPeminjaman")
    buku_regcomp = TextField("RegcompBuku", [Required()])
    peminjam_kode = TextField("KodePeminjam", [Required()])
    verified_by = HiddenField("VerifiedBy")
    tanggal_pinjam = TextField("TanggalPinjam", [Required()], default=get_datetime())
    tanggal_tenggat = TextField("TanggalTenggat", [Required()], default=get_datetime())
    status = SelectField(
        "Status",
        choices=peminjaman_code.get_status(),
        validators=[Required()],
        default='pinjam'
    )
