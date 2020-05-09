"""
Buku & Dewey Class
"""
from flask import url_for
from app import DB as db
from app.models import Base
from common import flash_code
from common.nlp_preprocess import NLP


class Buku(Base):

    __tablename__ = 'buku'

    reg_comp = db.Column(db.String(30), nullable=True)
    judul = db.Column(db.String(120), nullable=True)
    preprocessed_judul = db.Column(db.String(120), nullable=True)

    dewey_classification_kode = db.Column(db.Integer, nullable=True)

    def __init__(self, reg_comp, judul):
        self.reg_comp = reg_comp
        self.judul = judul

    def __repr__(self):
        return '<Buku %r>' % (self.reg_comp)

    def regcomp_available(reg_comp):
        return Buku.query.filter_by(reg_comp=reg_comp, is_delete=0).first()

    def get_buku(buku_id=None):
        if buku_id is None:
            return Buku.query.filter_by(is_delete=0).all()
        return Buku.query.filter_by(id=buku_id, is_delete=0).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def update(buku_id, reg_comp, judul):
        try:
            buku = Buku.query.filter_by(id=buku_id, is_delete=0).first()
            buku.reg_comp = reg_comp
            buku.judul = judul
            db.session.add(buku)
            db.session.commit()
            return True
        except:
            return False


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
