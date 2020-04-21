"""
Referensi's Models
"""
from app import DB as db
from app.models import Base
from common import flash_code


class Referensi(Base):
    
    __tablename__ = 'referensi'

    pengarang = db.Column(db.String(70), nullable=True)
    judul = db.Column(db.String(120), nullable=True)
    keterangan = db.Column(db.String(300), nullable=True)

    preprocessed_keterangan = db.Column(db.String(300), nullable=True)

    matakuliah_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, pengarang, judul, keterangan, matakuliah_id):
        self.pengarang = pengarang
        self.judul = judul
        self.keterangan = keterangan
        self.matakuliah_id = matakuliah_id

    def __repr__(self):
        return '<Referensi %r>' % (self.id)

    def get_by_matakuliah_id(matakuliah_id):
        return Referensi.query.filter_by(matakuliah_id=matakuliah_id, is_delete=0).all()
