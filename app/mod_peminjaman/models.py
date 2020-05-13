"""
Peminjaman Class
"""
from flask import url_for
from app import DB as db
from app.models import Base
from app.mod_buku.models import Buku
from app.mod_auth.models import Staff
from app.mod_mahasiswa.models import Mahasiswa
from common import flash_code


class Peminjaman(Base):

    __tablename__ = 'peminjaman_buku'


    buku_id = db.Column(db.Integer, nullable=False)
    mahasiswa_peminjaman_id = db.Column(db.Integer, nullable=True)
    staff_peminjam_id = db.Column(db.Integer, nullable=True)
    verified_by = db.Column(db.Integer, nullable=False)

    tanggal_pinjam = db.Column(db.DateTime, nullable=True)
    tanggal_tenggat = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(10), nullable=True)
    
    def __init__(self, verified_by, buku_regcomp, pemustaka_kode, tanggal_pinjam, tanggal_tenggat, status):
        self.verified_by = verified_by
        self.tanggal_pinjam = tanggal_pinjam
        self.tanggal_tenggat = tanggal_tenggat
        self.status = status
        self.set_buku(buku_regcomp)
        self.set_pemustaka(pemustaka_kode)

    def __repr__(self):
        return '<Peminjaman %r>' % (self.id)

    def set_buku(self, reg_comp):
        buku = Buku.query.filter_by(reg_comp=reg_comp, is_delete=0).first()
        self.buku_id = buku.id
    
    def check_buku(reg_comp):
        return Buku.regcomp_available(reg_comp)

    def set_pemustaka(self, kode_pemustaka):
        staff = Staff.query.filter_by(npk=kode_pemustaka, is_delete=0).first()
        if staff is not None:
            self.staff_peminjam_id = staff.id

        mahasiswa = Mahasiswa.query.filter_by(nrp=kode_pemustaka, is_delete=0).first()
        if mahasiswa is not None:
            self.mahasiswa_peminjaman_id = mahasiswa.id

    def check_pemustaka(kode_pemustaka):
        if Staff.query.filter_by(npk=kode_pemustaka, is_delete=0).first() is not None:
            return True
        elif Mahasiswa.query.filter_by(nrp=kode_pemustaka, is_delete=0).first() is not None:
            return True
        return False

    def get_peminjaman():
        return Peminjaman.query.filter_by(is_delete=0).all()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
