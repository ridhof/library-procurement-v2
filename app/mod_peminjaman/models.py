"""
Peminjaman Class
"""
from flask import url_for
import datetime
from datetime import timedelta
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.models import Base
from app.mod_buku.models import Buku
from app.mod_auth.models import Staff
from app.mod_mahasiswa.models import Mahasiswa
from app.mod_unit.models import Unit
from app.mod_peminjaman.tasks import read_excel
from common import flash_code, perpus_code


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

    def import_excel(path, sheet_index):
        try:
            task = rqueue.enqueue(
                read_excel,
                path,
                sheet_index,
                url_for('peminjaman.store')
            )
            return True
        except:
            return False

    def set_buku(self, reg_comp):
        buku = Buku.query.filter_by(reg_comp=reg_comp, is_delete=0).first()
        self.buku_id = buku.id
    
    def check_buku(reg_comp):
        return Buku.regcomp_available(reg_comp)

    def get_buku(self, is_preprocessed=False):
        try:
            buku = Buku.query.filter_by(id=self.buku_id, is_delete=0).first()
            result = buku.judul
            if is_preprocessed:
                preprocessed_dewey = buku.get_dewey(is_preprocessed=True)
                result = f"{preprocessed_dewey} {buku.preprocessed_judul}"
            return result
        except:
            return ''

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

    def get_pemustaka_object(kode_pemustaka):
        staff =  Staff.query.filter_by(npk=kode_pemustaka, is_delete=0).first()
        mahasiswa = Mahasiswa.query.filter_by(nrp=kode_pemustaka, is_delete=0).first()
        if staff is not None:
            return staff
        elif mahasiswa is not None:
            return mahasiswa
        return None

    def get_pemustaka(self):
        staff = Staff.query.filter_by(id=self.staff_peminjam_id, is_delete=0).first()
        if staff is not None:
            return f"Staff {staff.npk}"

        mahasiswa = Mahasiswa.query.filter_by(id=self.mahasiswa_peminjaman_id, is_delete=0).first()
        if mahasiswa is not None:
            return f"Mahasiswa {mahasiswa.nrp}"

    def get_latest_month_peminjaman():
        today = datetime.datetime.today()
        month = today.month - 1
        year = today.year
        if month < 1:
            month = 12
            year = year - 1
        prev_month = datetime.datetime(year, month, today.day)
        peminjamans = Peminjaman.query.filter(Peminjaman.tanggal_pinjam >= prev_month).all()
        return peminjamans
    
    def get_peminjaman(periode=None):
        if periode is None:
            return Peminjaman.query.filter_by(is_delete=0).all()
        
        peminjaman_query = Peminjaman.query.filter_by(is_delete=0).all()
        peminjamans = []
        for peminjaman in peminjaman_query:
            if peminjaman.tanggal_pinjam.strftime("%Y-%m") == periode:
                peminjamans.append(peminjaman)
        return peminjamans

    def get_periode():
        peminjamans = Peminjaman.query.filter_by(is_delete=0).all()
        periodes = []
        for peminjaman in peminjamans:
            tanggal = peminjaman.tanggal_pinjam.strftime("%Y-%m")
            if tanggal not in periodes:
                periodes.append(tanggal)
        return periodes
    
    def get_tanggal(self):
        tanggal = self.tanggal_pinjam.strftime("%Y-%m-%d")
        return tanggal

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def delete(peminjaman_id):
        try:
            peminjaman = Peminjaman.query.filter_by(id=peminjaman_id).first()
            peminjaman.is_delete = 1
            db.session.add(peminjaman)
            db.session.commit()
            return True
        except Exception:
            return False

    def store_peminjaman(reg_comp, judul, anggota_kode, tanggal_pinjam, tanggal_tenggat, status, petugas_nama):
        try:
            buku = Peminjaman.check_buku(reg_comp)
            if buku is None:
                buku = Buku(reg_comp, judul)
                if buku.insert() is False:
                    return False
            
            unit = Unit.query.filter_by(nama='sementara', is_delete=0).first()
            if unit is None:
                unit = Unit('99', 'sementara', 'S1', '1', '1')
                if unit.insert() is False:
                    return False

            pemustaka = Peminjaman.get_pemustaka_object(anggota_kode)
            if pemustaka is None:
                if len(anggota_kode) == 6:
                    pemustaka = Staff(anggota_kode, 'secret', f'pemustaka {anggota_kode}', unit.id, is_kalab=False, is_kajur=False, perpus_role=perpus_code.ANGGOTA)
                    if pemustaka.insert() is False:
                        return False
                else:
                    mahasiswa = Mahasiswa(unit_id=unit.id, nrp=anggota_kode, nama='')
                    if mahasiswa.insert() is False:
                        return False
                        
            pustakawan = Staff.get_by_name(petugas_nama)
            if pustakawan is None:
                pustakawan = Staff('', 'secret', petugas_nama, unit.id, False, False, perpus_code.PEGAWAI)
                if pustakawan.insert() is False:
                    return False
            
            tanggal_pinjam = tanggal_pinjam.split('/')
            tanggal_pinjam = datetime.datetime(int(tanggal_pinjam[2]), int(tanggal_pinjam[0]), int(tanggal_pinjam[1]))
            # print(tanggal_pinjam)
            # tanggal_pinjam = datetime.datetime.today()

            tanggal_tenggat = tanggal_tenggat.split('/')
            tanggal_tenggat = datetime.datetime(int(tanggal_tenggat[2]), int(tanggal_tenggat[0]), int(tanggal_tenggat[1]))
            # print(tanggal_tenggat)
            # tanggal_tenggat = datetime.datetime.today()

            peminjaman = Peminjaman(
                verified_by=pustakawan.id,
                buku_regcomp=buku.reg_comp,
                pemustaka_kode=anggota_kode,
                tanggal_pinjam=tanggal_pinjam,
                tanggal_tenggat=tanggal_tenggat,
                status=status
            )

            if peminjaman.insert() is False:
                return False
            return True
        except Exception:
            return False
