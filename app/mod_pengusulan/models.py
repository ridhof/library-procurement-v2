"""
Pengusulan's Models
"""
from app import DB as db
from app.models import Base
from common import flash_code


class Pengusulan(Base):

    __tablename__ = 'pengusulan_buku'

    pengarang = db.Column(db.String(70), nullable=True)
    judul = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(24), nullable=True)

    supplier = db.Column(db.String(70), nullable=True)
    harga = db.Column(db.Integer, nullable=True)

    tanggal_pengusulan = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    tanggal_disetujui_unit = db.Column(db.DateTime, nullable=True)
    tanggal_disetujui_direktur = db.Column(db.DateTime, nullable=True)
    tanggal_selesai = db.Column(db.DateTime, nullable=True)

    preprocessed_judul = db.Column(db.String(120))

    pengusul_id = db.Column(db.Integer, nullable=False)
    petugas_unit_id = db.Column(db.Integer, nullable=True)
    petugas_pustakawan_id = db.Column(db.Integer, nullable=True)

    def __init__(self, pengarang, judul, pengusul_id):
        self.pengarang = pengarang
        self.judul = judul
        self.pengusul_id = pengusul_id

    def __repr__(self):
        return '<Pengusulan %r>' % (self.id)

    def get_by_staff(staff_id):
        return Pengusulan.query.filter_by(pengusul_id=staff_id, is_delete=0).all()


class Relevansi(Base):

    __tablename__ = 'relevansi_detail'

    nilai_distance = db.Column(db.Float, nullable=True)

    pengusulan_buku_id = db.Column(db.Integer, nullable=False)
    matakuliah_id = db.Column(db.Integer, nullable=False)

    def __init__(self, pengusulan_buku_id, matakuliah_id):
        self.pengusulan_buku_id = pengusulan_buku_id
        self.matakuliah_id = matakuliah_id

    def __repr__(self):
        return '<Relevansi %r>' % (self.id)
