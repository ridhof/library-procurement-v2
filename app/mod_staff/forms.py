"""
Staff Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, TextField

from wtforms.validators import Required

class StaffForm(FlaskForm):
    """
    Forms to Create or Update Staff
    """
    staff_id = HiddenField("IdStaff")
    npk = TextField('NPK', [Required()])
    nama = TextField('Nama', [Required()])
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
