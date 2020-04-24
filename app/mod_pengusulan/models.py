"""
Pengusulan's Models
"""
from app import DB as db
from app.models import Base
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
        return self.status

    def get_by_staff(staff_id):
        return Pengusulan.query.filter_by(pengusul_id=staff_id, is_delete=0).all()

    def insert(self, matakuliah_ids=[]):
        try:
            self.status = pengusulan_code.DIUSULKAN
            db.session.add(self)
            db.session.commit()

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
