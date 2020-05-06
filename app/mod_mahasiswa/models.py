"""
Mahasiswa's Models
"""
from flask import url_for
from app import DB as db
from app.models import Base
from common import flash_code


class Mahasiswa(Base):

    __tablename__ = 'mahasiswa'

    nrp = db.Column(db.String(10), nullable=True)
    nama = db.Column(db.String(70), nullable=True)

    unit_id = db.Column(db.Integer, nullable=False)

    def __init__(self, unit_id, nrp, nama=None):
        self.unit_id = unit_id
        self.nrp = nrp

        if nama is not None:
            self.nama = nama

    def __repr__(self):
        return '<Mahasiswa %r>' % (self.nrp)

    def get_by_unit(unit_id):
        return Mahasiswa.query.filter_by(unit_id=unit_id, is_delete=0).all()

