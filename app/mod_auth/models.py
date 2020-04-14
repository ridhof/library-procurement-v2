"""
Auth's Models contains Base and Staff Object
"""
from flask import flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import DB as db
from app.models import Base
from app.mod_unit.models import Unit
from common import code, flash_code, perpus_code


class Staff(Base):
    """
    Staff Class
    """

    __tablename__ = 'staff'

    npk = db.Column(db.String(6), nullable=True)
    password = db.Column(db.String(192), nullable=True)
    nama = db.Column(db.String(70), nullable=True)
    unit_id = db.Column(db.Integer, nullable=False)
    is_kalab = db.Column(db.Boolean, nullable=True)
    is_kajur = db.Column(db.Boolean, nullable=True)
    perpus_role = db.Column(db.String(8), nullable=True)

    def __init__(self, npk, password, nama, unit_id, is_kalab, is_kajur, perpus_role):
        self.npk = npk
        self.password = generate_password_hash(password)
        self.nama = nama
        self.unit_id = unit_id
        self.is_kalab = is_kalab
        self.is_kajur = is_kajur
        self.perpus_role = perpus_role

    def __repr__(self):
        return '<Staff %r>' % (self.nama)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def login(npk, password):
        staff = Staff.query.filter_by(npk=npk, is_delete=0).first()
        if staff:
            if staff.check_password(password):
                return {"status": code.OK, "staff": staff}
        return {"status": code.AUTHORIZATION_ERROR}

    def is_login():
        user = None
        if session.get('user_id') is None:
            flash("Silahkan login terlebih dahulu", flash_code.WARNING)
        else:
            user_id = session.get('user_id')
            user = Staff.query.filter_by(id=user_id).first()
        return user

    def is_role(self, role):
        if self.perpus_role is role:
            flash("Akun anda tidak dapat mengakses/melakukan hal tersebut", flash_code.WARNING)
            return False
        return True

    def get_unit(self):
        return Unit.query.filter_by(kode=self.unit_id).first()

    def get_all():
        return Staff.query.filter_by(is_delete=0).all()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
