"""
Landing Page Module's Controllers
"""
from flask import Blueprint, send_from_directory

MOD_LANDING_PAGE = Blueprint('landing_page', __name__, url_prefix='/')


@MOD_LANDING_PAGE.route('/robots.txt', methods=['GET'])
def robots():
    """
    Return robot.txt file.
    """
    return send_from_directory('static/', filename='robots.txt')
