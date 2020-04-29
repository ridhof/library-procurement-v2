"""
RPS's Models
"""
from flask import url_for
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.mod_rps.tasks import preprocess_rps
from app.models import Base
from common import flash_code


class Rps(Base):

    __tablename__ = 'rps_detail'

    kompetensi_dasar = db.Column(db.String(200), nullable=True)
    indikator_capaian = db.Column(db.String(200), nullable=True)
    materi = db.Column(db.String(200), nullable=True)

    preprocessed_kompetensi = db.Column(db.String(200), nullable=True)
    preprocessed_indikator = db.Column(db.String(200), nullable=True)
    preprocessed_materi = db.Column(db.String(200), nullable=True)

    matakuliah_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, kompetensi_dasar, indikator_capaian, materi, matakuliah_id):
        self.kompetensi_dasar = kompetensi_dasar
        self.indikator_capaian = indikator_capaian
        self.materi = materi
        self.matakuliah_id = matakuliah_id

    def __repr__(self):
        return '<Referensi %r>' % (self.id)

    def get_by_matakuliah_id(matakuliah_id):
        return Rps.query.filter_by(matakuliah_id=matakuliah_id, is_delete=0).all()

    def get_by_id(rps_id):
        return Rps.query.filter_by(id=rps_id, is_delete=0).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()

            task = rqueue.enqueue(
                preprocess_rps,
                self.kompetensi_dasar,
                self.indikator_capaian,
                self.materi,
                url_for('rps.store_preprocess', rps_id=self.id)
            )

            return True
        except:
            return False

    def update(rps_id, kompetensi_dasar=None, indikator_capaian=None, materi=None):
        try:
            rps = Rps.query.filter_by(id=rps_id, is_delete=0).first()
            if kompetensi_dasar is not None:
                rps.kompetensi_dasar = kompetensi_dasar
            if indikator_capaian is not None:
                rps.indikator_capaian = indikator_capaian
            if materi is not None:
                rps.materi = materi
            db.session.add(rps)
            db.session.commit()

            task = rqueue.enqueue(
                preprocess_rps,
                rps.kompetensi_dasar,
                rps.indikator_capaian,
                rps.materi,
                url_for('rps.store_preprocess', rps_id=rps.id)
            )

            return True
        except:
            return False

    def delete(rps_id):
        try:
            rps = Rps.query.filter_by(id=rps_id).first()
            rps.is_delete = 1
            db.session.add(rps)
            db.session.commit()
            return True
        except Exception:
            return False

    def store_preprocessed(rps_id, preprocessed_kompetensi, preprocessed_indikator, preprocessed_materi):
        try:
            rps = Rps.query.filter_by(id=rps_id).first()
            rps.preprocessed_kompetensi = preprocessed_kompetensi
            rps.preprocessed_indikator = preprocessed_indikator
            rps.preprocessed_materi = preprocessed_materi
            db.session.add(rps)
            db.session.commit()
            return True
        except Exception:
            return False
