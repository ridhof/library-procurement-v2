"""
Peminjaman Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_peminjaman.models import Peminjaman

from common import flash_code

MOD_PEMINJAMAN = Blueprint('peminjaman', __name__, url_prefix='/peminjaman/')

@MOD_PEMINJAMAN.route('', methods=['GET'])
def table():
    """
    Return Peminjaman Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    peminjamans = Peminjaman.get_peminjaman()
    return render_template("peminjaman/table.html", peminjamans=peminjamans, user=user)
