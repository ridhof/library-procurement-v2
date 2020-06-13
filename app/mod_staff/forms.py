"""
Staff Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, SelectField, TextField

from wtforms.validators import Required
from common import perpus_code


class StaffForm(FlaskForm):
    """
    Forms to Create or Update Staff
    """
    staff_id = HiddenField("IdStaff")
    npk = TextField('NPK', [Required()])
    nama = TextField('Nama', [Required()])
    unit_id = TextField('UnitId', default='')
    role = SelectField(
        'Role',
        choices=[
            ('staff', 'Staff'),
            ('kalab', 'Kepala Lab'),
            ('kajur', 'Ketua Jurusan')
        ],
        validators=[Required()],
        default='staff'
    )
    perpus_role = SelectField(
        'PerpusRole',
        choices=[
            (perpus_code.ANGGOTA, 'Pemustaka'),
            (perpus_code.PEGAWAI, 'Pegawai'),
            (perpus_code.KEPALA_BAGIAN, 'Kepala Bagian'),
            (perpus_code.DIREKTUR, 'Direktur')
        ],
        default=perpus_code.ANGGOTA
    )


class PasswordForm(FlaskForm):
    """
    Forms to Change Password
    """
    staff_id = HiddenField("IdStaff")
    password = PasswordField("Password", [Required()])
    repassword = PasswordField("Repassword", [Required()])
