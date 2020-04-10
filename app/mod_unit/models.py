"""
Unit's Models
"""
from app import DB as db
from app.models import Base


class Unit(Base):

    __tablename__ = 'unit'

    kode = db.Column(db.String(2), nullable=False)
    nama = db.Column(db.String(64), nullable=True)
    gedung = db.Column(db.String(24), nullable=True)
    lantai = db.Column(db.String(2), nullable=True)
    ruangan = db.Column(db.String(3), nullable=True)

    def __repr__(self):
        return '<Unit %r>' % (self.kode)
