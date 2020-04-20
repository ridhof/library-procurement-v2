"""
Matakuliah's Models
"""
from app import DB as db
from app.models import Base
from common import flash_code


class Matakuliah(Base):

    __tablename__ = 'matakuliah'

    kode = db.Column(db.String(10), nullable=False)
    nama = db.Column(db.String(60), nullable=True)
    sks = db.Column(db.Integer, nullable=True)
    deskripsi_singkat = db.Column(db.String(200), nullable=True)
    standar_kompetensi = db.Column(db.String(200), nullable=True)

    preprocessed_deskripsi = db.Column(db.String(200), nullable=True)
    preprocessed_standar = db.Column(db.String(200), nullable=True)

    unit_id = db.Column(db.Integer, nullable=False)
    kurikulum = db.Column(db.String(12), nullable=True)
    
    def __init__(self, kode, nama, sks, deskripsi_singkat, standar_kompetensi, unit_id, kurikulum):
        self.kode = kode
        self.nama = nama
        self.sks = sks
        self.deskripsi_singkat = deskripsi_singkat
        self.standar_kompetensi = standar_kompetensi
        self.unit_id = unit_id
        self.set_kurikulum(kurikulum)

    def __repr__(self):
        return '<Matakuliah %r>' % (self.kode)

    def set_kurikulum(self, kurikulum):
        temp_kurikulum = kurikulum.split('-')[1]
        temp_tahun = kurikulum.split('-')[0].split('/')
        self.kurikulum = f"{temp_tahun[0][2:]}/{temp_tahun[1][2:]}-{temp_kurikulum}"

    def get_kurikulum(self):
        temp_kurikulum = self.kurikulum.split('-')[1]
        temp_tahun = self.kurikulum.split('-')[0].split('/')
        return f"20{temp_tahun[0]}/20{temp_tahun[1]} {temp_kurikulum.upper()}"

    def get_by_unit(unit_id):
        return Matakuliah.query.filter_by(unit_id=unit_id, is_delete=0).all()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
