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
    deskripsi_singkat = db.Column(db.String(600), nullable=True)
    standar_kompetensi = db.Column(db.String(600), nullable=True)

    preprocessed_deskripsi = db.Column(db.String(600), nullable=True)
    preprocessed_standar = db.Column(db.String(600), nullable=True)

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

    def get_by_kode(matakuliah_id, kode):
        return Matakuliah.query.filter_by(id=matakuliah_id, kode=kode, is_delete=0).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def update(matakuliah_id, kode=None, nama=None, sks=None, deskripsi_singkat=None, standar_kompetensi=None, tahun_ajaran=None, kurikulum=None):
        try:
            matakuliah = Matakuliah.query.filter_by(id=matakuliah_id, is_delete=0).first()
            if kode is not None:
                matakuliah.kode = kode
            if nama is not None:
                matakuliah.nama = nama
            if sks is not None:
                matakuliah.sks = sks
            if deskripsi_singkat is not None:
                matakuliah.deskripsi_singkat = deskripsi_singkat
            if standar_kompetensi is not None:
                matakuliah.standar_kompetensi = standar_kompetensi
            if tahun_ajaran is not None and kurikulum is not None:
                matakuliah.set_kurikulum(f"{tahun_ajaran}-{kurikulum}")
            db.session.add(matakuliah)
            db.session.commit()
            return True
        except:
            return False
