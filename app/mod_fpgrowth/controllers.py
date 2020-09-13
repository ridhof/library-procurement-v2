"""
FPGrowth Module's Controllers
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.mod_auth.models import Staff
from app.mod_clustering.models import Clustering, PeminjamanClustering
from app.mod_fpgrowth.models import FrequentPatternGrowth
from app.mod_peminjaman.models import Peminjaman
from common import flash_code


MOD_FPGROWTH = Blueprint('fpgrowth', __name__, url_prefix='/fpgrowth/')

@MOD_FPGROWTH.route('', methods=['GET', 'POST'])
def table():
    """
    Return Main FPGrowth Page
    """
    if request.method == 'GET':
        clustering_id = request.args.get('clustering_id')
        clusterings = Clustering.find(clustering_id)
        if clusterings is not None:
            tahun = clusterings.tahun
            bulan = clusterings.bulan
            if len(f"{bulan}") == 1:
                bulan = f"0{bulan}"
            peminjamans = Peminjaman.get_peminjaman(periode=f"{tahun}-{bulan}")
            peminjamans_dicts = []
            for peminjaman in peminjamans:
                pemustaka = peminjaman.get_pemustaka()
                tanggal_pinjam = peminjaman.get_tanggal()
                buku_id = peminjaman.buku_id
                peminjaman_clustering_id =  PeminjamanClustering.get_id(buku_id, clustering_id)
                if peminjaman_clustering_id is not None:
                    peminjamans_dicts.append({
                        'pemustaka': pemustaka, 
                        'tanggal_pinjam': tanggal_pinjam, 
                        'peminjaman_clustering_id': peminjaman_clustering_id
                    })
            print(FrequentPatternGrowth.helper(peminjamans_dicts))
            return f"FPGrowth Trigger Enabled!"
        else:
            user = Staff.is_login()
            if user is None:
                return redirect(url_for('auth.login'))

            periode = request.args.get('periode')
            fpgrowths = FrequentPatternGrowth.get(periode=periode)
            return render_template("fpgrowth/table.html", fpgrowths=fpgrowths, periode=periode)
    else:
        main_itemset = request.form['main_itemset']
        correlated_itemset = request.form['correlated_itemset']
        confidence_value = request.form['confidence_value']
        support_value = request.form['support_value']
        lift_value = request.form['lift_value']

        frequentPatternGrowth = FrequentPatternGrowth(confidence_value, support_value, lift_value, main_itemset, correlated_itemset)
        if frequentPatternGrowth.insert():
            print(f"Berhasil menyimpan {main_itemset} dan {correlated_itemset}")
        else:
            print(f"Gagal menyimpan {main_itemset} dan {correlated_itemset}")
        return f"FPGrowth POST!"
