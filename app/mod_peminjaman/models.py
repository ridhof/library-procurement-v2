"""
Peminjaman Class
"""
from flask import url_for
from app import DB as db
from app.models import Base
from common import flash_code


class Peminjaman(Base):

    __tablename__ = 'peminjaman_buku'


    buku_id = db.Column(db.Integer, nullable=False)
    mahasiswa_peminjaman_id = db.Column(db.Integer, nullable=False)
    staff_peminjam_id = db.Column(db.Integer, nullable=False)
    verified_by = db.Column(db.Integer, nullable=False)

    tanggal_pinjam = db.Column(db.DateTime, nullable=True)
    tanggal_tenggat = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(10), nullable=True)
    
    def __init__(self, verified_by):
        self.verified_by = verified_by

    def __repr__(self):
        return '<Peminjaman %r>' % (self.id)

    def get_peminjaman():
        return Peminjaman.query.filter_by(is_delete=0).all()

