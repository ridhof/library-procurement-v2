"""
App module contains main application of Flask.
"""
from flask import Flask, render_template, abort, jsonify
import flask_restful
from flask_sqlalchemy import SQLAlchemy
import redis
from rq import Queue

from common import code, pretty_result

APP = Flask(__name__)

HANDLE_EXCEPTION = APP.handle_exception
HANDLE_USER_EXCEPTION = APP.handle_user_exception

DB = SQLAlchemy(APP)

REDIS = redis.Redis()
REDIS_QUEUE = Queue(connection=REDIS, default_timeout=6000)

def _custom_abort(http_status_code, **kwargs):
    if http_status_code == 400:
        message = kwargs.get('message')
        if isinstance(message, dict):
            param, info = list(message.items())[0]
            data = '{}:{}!'.format(param, info)
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=data)))
        else:
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=message)))
    return abort(http_status_code)

def _access_control(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response

def create_app(config):
    """
    Function to create the flask app.
    """
    # Configurations
    APP.config.from_object(config)
    APP.after_request(_access_control)
    flask_restful.abort = _custom_abort

    # Sample HTTP error and handling
    @APP.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_landing_page.controllers import MOD_LANDING_PAGE as landing_page_module
    from app.mod_auth.controllers import MOD_AUTH as auth_module
    from app.mod_dashboard.controllers import MOD_DASHBOARD as dashboard_module
    from app.mod_unit.controllers import MOD_UNIT as unit_module
    from app.mod_staff.controllers import MOD_STAFF as staff_module
    from app.mod_matakuliah.controllers import MOD_MATAKULIAH as matakuliah_module
    from app.mod_referensi.controllers import MOD_REFERENSI as referensi_module
    from app.mod_rps.controllers import MOD_RPS as rps_module
    from app.mod_pengusulan.controllers import MOD_PENGUSULAN as pengusulan_module
    from app.mod_mahasiswa.controllers import MOD_MAHASISWA as mahasiswa_module
    from app.mod_buku.controllers import MOD_BUKU as buku_module
    from app.mod_peminjaman.controllers import MOD_PEMINJAMAN as peminjaman_module
    from app.mod_clustering.controllers import MOD_CLUSTERING as clustering_module
    from app.mod_fpgrowth.controllers import MOD_FPGROWTH as fpgrowth_module
    from app.mod_perceptron.controllers import MOD_PERCEPTRON as perceptron_module

    # Register blueprints
    APP.register_blueprint(landing_page_module)
    APP.register_blueprint(auth_module)
    APP.register_blueprint(dashboard_module)
    APP.register_blueprint(unit_module)
    APP.register_blueprint(staff_module)
    APP.register_blueprint(matakuliah_module)
    APP.register_blueprint(referensi_module)
    APP.register_blueprint(rps_module)
    APP.register_blueprint(pengusulan_module)
    APP.register_blueprint(mahasiswa_module)
    APP.register_blueprint(buku_module)
    APP.register_blueprint(peminjaman_module)
    APP.register_blueprint(clustering_module)
    APP.register_blueprint(fpgrowth_module)
    APP.register_blueprint(perceptron_module)

    # Build the database:
    # This will create the database file using SQLAlchemy
    # db.create_all()
    DB.init_app(APP)

    APP.handle_exception = HANDLE_EXCEPTION
    APP.handle_user_exception = HANDLE_USER_EXCEPTION
    return APP
