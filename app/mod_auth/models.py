"""
Auth's Models contains Base and Staff Object
"""
from flask import flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import DB as db
from app.models import Base
from app.mod_unit.models import Unit
from common import code, flash_code, perpus_code, config


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
            user = Staff.query.filter_by(id=user_id, is_delete=0).first()
        return user

    def is_pustakawan(self):
        if self.perpus_role == perpus_code.ANGGOTA:
            return False
        return True

    def is_role(self, role):
        if self.perpus_role != role:
            flash("Akun anda tidak dapat mengakses atau melakukan hal tersebut", flash_code.WARNING)
            return False
        return True

    def is_superadmin(self):
        if self.npk == config.SUPERADMIN_USERNAME:
            return True
        return False

    def get_unit_role(self):
        role = 'staff'
        if self.is_kajur:
            role = 'kajur'
        elif self.is_kalab:
            role = 'kalab'
        return role

    def get_unit(self):
        return Unit.query.filter_by(kode=self.unit_id, is_delete=0).first()

    def get_all():
        return Staff.query.filter_by(is_delete=0).all()

    def get_pustakawans():
        pustakawans = []
        pustakawans.extend(Staff.query.filter_by(perpus_role=perpus_code.PEGAWAI, is_delete=0).all())
        pustakawans.extend(Staff.query.filter_by(perpus_role=perpus_code.KEPALA_BAGIAN, is_delete=0).all())
        pustakawans.extend(Staff.query.filter_by(perpus_role=perpus_code.DIREKTUR, is_delete=0).all())
        return pustakawans

    def find(id):
        return Staff.query.filter_by(id=id, is_delete=0).first()

    def get_by_unit(unit_id):
        return Staff.query.filter_by(unit_id=unit_id, is_delete=0).all()

    def get_by_npk(staff_id, npk):
        return Staff.query.filter_by(id=staff_id, npk=npk, is_delete=0).first()

    def get_by_name(nama):
        return Staff.query.filter_by(nama=nama, is_delete=0).first()

    def get_npk(self):
        npk = self.npk
        if npk == '':
            npk = 'NPK belum didaftarkan'
        return npk

    def get_form_data(self, is_superadmin=False, is_pustakawan=False):
        form_data = {
            'staff_id': self.id,
            'npk': self.npk,
            'nama': self.nama,
            'role': self.get_unit_role()
        }

        if is_superadmin:
            form_data['perpus_role'] = self.perpus_role
            form_data['unit_id'] = self.unit_id

        if is_pustakawan:
            form_data['perpus_role'] = self.perpus_role
        
        return form_data

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def update(staff_id, npk=None, nama=None, role=None, unit_id=None, perpus_role=None):
        try:
            staff = Staff.query.filter_by(id=staff_id, is_delete=0).first()

            if npk is not None:
                staff.npk = npk
            if nama is not None:
                staff.nama = nama
            if role is not None:
                staff.is_kajur = 0
                staff.is_kalab = 0
                if role == 'kajur':
                    staff.is_kajur = 1
                elif role == 'kalab':
                    staff.is_kalab = 1
            if unit_id is not None:
                staff.unit_id = unit_id
            if perpus_role is not None:
                staff.perpus_role = perpus_role 
            db.session.add(staff)
            db.session.commit()
            return True
        except:
            return False

    def delete(staff_id):
        try:
            staff = Staff.query.filter_by(id=staff_id).first()
            staff.is_delete = 1
            db.session.add(staff)
            db.session.commit()
            return True
        except:
            return False

    def change_password(self, new_password):
        try:
            self.set_password(new_password)
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
