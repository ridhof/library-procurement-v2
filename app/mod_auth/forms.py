"""
Auth Module's Forms
"""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

from wtforms.validators import Required


class LoginForm(FlaskForm):
    """
    Forms used to Login
    """
    npk = TextField(
        'NPK', [Required(message="Apakah anda lupa dengan NPK anda?")])
    password = PasswordField(
        'Password', [Required(message="Password harus diisi!")])
