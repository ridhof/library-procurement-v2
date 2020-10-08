"""
Perceptron Module's Controllers
"""
from flask import Blueprint, request
from app.mod_clustering.models import Clustering, PeminjamanClustering
from app.mod_peminjaman.models import Peminjaman
from app.mod_perceptron.models import Perceptron


MOD_PERCEPTRON = Blueprint('perceptron', __name__, url_prefix='/perceptron/')

@MOD_PERCEPTRON.route('', methods=['GET', 'POST'])
def table():
    """
    Return Main Perceptron Page
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
                peminjaman_clustering_id = PeminjamanClustering.get_id(buku_id, clustering_id)
                peminjaman_clustering = PeminjamanClustering.find(peminjaman_clustering_id)
                if peminjaman_clustering_id is not None:
                    peminjamans_dicts.append({
                        'pemustaka': pemustaka,
                        'tanggal_pinjam': tanggal_pinjam,
                        'peminjaman_clustering_id': peminjaman_clustering.clustering_detail_id
                    })
            print(Perceptron.helper(peminjamans_dicts))
            return f"Perceptron Trigger Enabled!"
    else:
        cluster_id = request.form['cluster_id']
        priority_value = request.form['priority_value']

        perceptron = Perceptron(cluster_id, priority_value)
        if perceptron.insert():
            print(f"Berhasil menyimpan {cluster_id} dengan nilai {priority_value}")
        else:
            print(f"Gagal menyimpan {cluster_id} dengan nilai {priority_value}")
        return f"Perceptron POST!"
