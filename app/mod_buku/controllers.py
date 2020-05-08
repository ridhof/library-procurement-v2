"""
Buku Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.mod_auth.models import Staff
from app.mod_buku.models import Dewey

from common import flash_code

MOD_BUKU = Blueprint('buku', __name__, url_prefix='/buku/')

@MOD_BUKU.route('dewey/baru', methods=['POST'])
def store_dewey():
    """
    Store Dewey
    """
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        preprocessed_nama = request.form['preprocessed_nama']

        dewey = Dewey(kode, nama, preprocessed_nama=preprocessed_nama)
        if dewey.insert():
            return f"Berhasil melakukan penyimpanan data"
    return f"Gagal melakukan penyimpanan data"


