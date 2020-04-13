"""
Unit's Models
"""
from app import DB as db
from app.models import Base
from common import flash_code


class Unit(Base):

    __tablename__ = 'unit'

    kode = db.Column(db.String(2), nullable=False)
    nama = db.Column(db.String(64), nullable=True)
    gedung = db.Column(db.String(24), nullable=True)
    lantai = db.Column(db.String(2), nullable=True)
    ruangan = db.Column(db.String(3), nullable=True)

    def __init__(self, kode, nama, gedung, lantai, ruangan):
        self.kode = kode
        self.nama = nama
        self.gedung = gedung
        self.lantai = lantai
        self.ruangan = ruangan

    def __repr__(self):
        return '<Unit %r>' % (self.kode)

    def get_all():
        return Unit.query.filter_by(is_delete=0).all()

    def get_by_kode(unit_id, kode):
        return Unit.query.filter_by(id=unit_id, kode=kode, is_delete=0).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def update(unit_id, kode_unit=None, nama=None, gedung=None, lantai=None, ruangan=None):
        try:
            unit = Unit.query.filter_by(id=unit_id, is_delete=0).first()
            if kode_unit is not None:
                unit.kode = kode_unit
            if nama is not None:
                unit.nama = nama
            if gedung is not None:
                unit.gedung = gedung
            if lantai is not None:
                unit.lantai = lantai
            if ruangan is not None:
                unit.ruangan = ruangan
            db.session.add(unit)
            db.session.commit()
            return True
        except:
            return False

    def delete(unit_id):
        try:
            unit = Unit.query.filter_by(id=unit_id).first()
            unit.is_delete = 1
            db.session.add(unit)
            db.session.commit()
            return True
        except Exception:
            return False
