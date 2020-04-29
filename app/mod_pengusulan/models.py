"""
Pengusulan's Models
"""
import datetime
from flask import url_for

from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.mod_pengusulan.tasks import preprocess_pengusulan
from app.models import Base
from app.mod_auth.models import Staff
from common import flash_code, pengusulan_code


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

    def display_status(self):
        if self.status == pengusulan_code.DIUSULKAN:
            return 'Menunggu Verifikasi Kepala Unit'
        elif self.status == pengusulan_code.DISETUJUI_UNIT:
            return 'Menunggu Verifikasi Unit Perpustakaan'
        elif self.status == pengusulan_code.DITOLAK_UNIT:
            return 'Pengusulan Ditolak'
        return self.status

    def display_pengusul(self):
        staff = Staff.query.filter_by(id=self.pengusul_id).first()
        return f"{ staff.npk } - { staff.nama }"

    def get_by_unit(unit_id, status=pengusulan_code.DIUSULKAN):
        staffs = Staff.query.filter_by(unit_id=unit_id, is_delete=0).all()
        pengusulans = []

        if status == pengusulan_code.DIUSULKAN:
            for staff in staffs:
                for pengusulan in Pengusulan.query.filter_by(pengusul_id=staff.id, status=status, is_delete=0).all():
                    pengusulans.append(pengusulan)
        else:
            for staff in staffs:
                for pengusulan in Pengusulan.query.filter_by(pengusul_id=staff.id, is_delete=0).all():
                    pengusulans.append(pengusulan)
        return pengusulans
        
    def get_by_staff(staff_id):
        return Pengusulan.query.filter_by(pengusul_id=staff_id, is_delete=0).all()

    def insert(self, matakuliah_ids=[]):
        try:
            self.status = pengusulan_code.DIUSULKAN
            db.session.add(self)
            db.session.commit()

            task = rqueue.enqueue(
                preprocess_pengusulan,
                self.judul,
                url_for('pengusulan.store_preprocess', pengusulan_id=self.id)
            )

            if Relevansi.bulk_insert(pengusulan_id=self.id, matakuliah_ids=matakuliah_ids):
                return True
            return False
        except:
            return False

    def delete(pengusulan_id):
        try:
            pengusulan = Pengusulan.query.filter_by(id=pengusulan_id).first()
            pengusulan.is_delete = 1
            db.session.add(pengusulan)
            db.session.commit()
            return True
        except Exception:
            return False

    def approve(pengusulan_id, status, petugas_id):
        try:
            pengusulan = Pengusulan.query.filter_by(id=pengusulan_id, is_delete=0).first()
            if pengusulan.status != pengusulan_code.DIUSULKAN:
                return False
            
            if status == pengusulan_code.DISETUJUI_UNIT:
                pengusulan.status = pengusulan_code.DISETUJUI_UNIT
                pengusulan.tanggal_disetujui_unit = datetime.datetime.now()
            elif status == pengusulan_code.DITOLAK_UNIT:
                pengusulan.status = pengusulan_code.DITOLAK_UNIT
                pengusulan.tanggal_selesai = datetime.datetime.now()
            pengusulan.petugas_unit_id = petugas_id

            db.session.add(pengusulan)
            db.session.commit()
            return True
        except Exception:
            return False

    def store_preprocessed(pengusulan_id, preprocessed_judul):
        try:
            pengusulan = Pengusulan.query.filter_by(id=pengusulan_id).first()
            pengusulan.preprocessed_judul = preprocessed_judul
            db.session.add(pengusulan)
            db.session.commit()
            return True
        except Exception:
            return False


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

    def bulk_insert(pengusulan_id, matakuliah_ids=[]):
        try:
            list_relevansi = []
            for matakuliah_id in matakuliah_ids:
                relevansi = Relevansi(pengusulan_id, matakuliah_id)
                list_relevansi.append(relevansi)
            db.session.bulk_save_objects(list_relevansi)
            db.session.commit()
            return True
        except:
            return False
