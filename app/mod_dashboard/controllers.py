"""
Dashboard Module's Controllers
"""
from flask import Blueprint, redirect, render_template, url_for

from app.mod_auth.models import Staff

MOD_DASHBOARD = Blueprint('dashboard', __name__, url_prefix='/dashboard')
@MOD_DASHBOARD.route('', methods=['GET'])
def dashboard():
    """
    Return dashboard page
    """
    if Staff.is_login() is None:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/dashboard.html')
