"""
Buku & Dewey Class
"""
from flask import url_for
from app import DB as db
from app.models import Base
from common import flash_code
from common.nlp_preprocess import NLP


class Dewey(Base):

    __tablename__ = 'dewey_classification'

    # kode, nama 120, preprocessed_nama 120
    kode = db.Column(db.Integer, nullable=True)
    nama = db.Column(db.String(120), nullable=True)
    preprocessed_nama = db.Column(db.String(120), nullable=True)

    def __init__(self, kode, nama, preprocessed_nama=None):
        self.kode = kode
        self.nama = nama
        self.preprocessed_nama = preprocessed_nama

        if self.preprocessed_nama is None:
            nlp = NLP(self.nama)
            self.preprocessed_nama = nlp.preprocessed_text
    
    def __repr__(self):
        return '<Dewey %r>' % (self.kode)

    def kode_available(self):
        return Dewey.query.filter_by(kode=self.kode, is_delete=0).first()

    def insert(self):
        try:
            if self.kode_available() is not None:
                return False

            db.session.add(self)
            db.session.commit()
            return True
        except Exception:
            return False
