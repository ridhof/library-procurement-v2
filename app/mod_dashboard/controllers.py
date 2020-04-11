"""
Dashboard Module's Controllers
"""
from flask import Blueprint, render_template

MOD_DASHBOARD = Blueprint('dashboard', __name__, url_prefix='/dashboard')
@MOD_DASHBOARD.route('', methods=['GET'])
def dashboard():
    """
    Return dashboard page
    """
    return render_template('dashboard/dashboard.html')
