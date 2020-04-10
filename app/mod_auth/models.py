"""
Auth's Models contains Base and Staff Object
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app import DB as db
from app.models import Base
from app.mod_unit.models import Unit
from common import perpus_code, code


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

    def __init__(self, npk, password):
        self.npk = npk
        self.password = generate_password_hash(password)
        self.unit_id = 1

    def __repr__(self):
        return '<Staff %r>' % (self.nama)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def login(npk, password):
        staff = Staff.query.filter_by(npk=npk).first()
        if staff:
            if staff.check_password(password):
                return {"status": code.OK, "staff": staff}
        return {"status": code.AUTHORIZATION_ERROR}

    def get_unit(self):
        return Unit.query.filter_by(kode=self.unit_id).first()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return {'status': 'error'}
