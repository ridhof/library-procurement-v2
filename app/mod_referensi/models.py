"""
Referensi's Models
"""
from flask import url_for
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.mod_referensi.tasks import preprocess_referensi
from app.models import Base
from common import flash_code


class Referensi(Base):
    
    __tablename__ = 'referensi'

    pengarang = db.Column(db.String(70), nullable=True)
    judul = db.Column(db.String(120), nullable=True)
    keterangan = db.Column(db.String(300), nullable=True)

    preprocessed_keterangan = db.Column(db.String(300), nullable=True)

    matakuliah_id = db.Column(db.Integer, nullable=False)
    
    def __init__(self, pengarang, judul, keterangan, matakuliah_id):
        self.pengarang = pengarang
        self.judul = judul
        self.keterangan = keterangan
        self.matakuliah_id = matakuliah_id

    def __repr__(self):
        return '<Referensi %r>' % (self.id)

    def get_by_matakuliah_id(matakuliah_id):
        return Referensi.query.filter_by(matakuliah_id=matakuliah_id, is_delete=0).all()

    def get_by_id(referensi_id):
        return Referensi.query.filter_by(id=referensi_id, is_delete=0).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            task = rqueue.enqueue(
                preprocess_referensi,
                self.pengarang,
                self.judul,
                url_for('referensi.store_preprocess', referensi_id=self.id)
            )
            return True
        except:
            return False

    def update(referensi_id, pengarang=None, judul=None, keterangan=None):
        try:
            referensi = Referensi.query.filter_by(id=referensi_id, is_delete=0).first()
            if pengarang is not None:
                referensi.pengarang = pengarang
            if judul is not None:
                referensi.judul = judul
            if keterangan is not None:
                referensi.keterangan = keterangan
            db.session.add(referensi)
            db.session.commit()

            task = rqueue.enqueue(
                preprocess_referensi,
                referensi.pengarang,
                referensi.judul,
                url_for('referensi.store_preprocess', referensi_id=referensi.id)
            )

            return True
        except:
            return False

    def delete(referensi_id):
        try:
            referensi = Referensi.query.filter_by(id=referensi_id).first()
            referensi.is_delete = 1
            db.session.add(referensi)
            db.session.commit()
            return True
        except Exception:
            return False

    def store_preprocessed(referensi_id, preprocessed_keterangan):
        try:
            referensi = Referensi.query.filter_by(id=referensi_id).first()
            referensi.preprocessed_keterangan = preprocessed_keterangan
            db.session.add(referensi)
            db.session.commit()
            return True
        except Exception:
            return False
