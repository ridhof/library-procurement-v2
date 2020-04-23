"""
Pengusulan Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_pengusulan.models import Pengusulan, Relevansi

from common import flash_code


MOD_PENGUSULAN = Blueprint('pengusulan', __name__, url_prefix='/pengusulan/')


@MOD_PENGUSULAN.route('', methods=['GET'])
def table():
    """
    Return Pengusulan Table Page
    """
    user = Staff.is_login()
    if user is None:
        return redirect(url_for('auth.login'))

    pengusulans = Pengusulan.get_by_staff(user.id)
    return render_template("pengusulan/table.html", pengusulans=pengusulans)
