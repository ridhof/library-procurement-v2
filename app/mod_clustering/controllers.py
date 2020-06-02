"""
Clustering Module's Controllers
"""
from flask import Blueprint, request
from datetime import datetime
from app.mod_peminjaman.models import Peminjaman
from app.mod_clustering.models import Clustering, ClusteringDetail, PeminjamanClustering

from common import flash_code

MOD_CLUSTERING = Blueprint('clustering', __name__, url_prefix='/clustering/')

@MOD_CLUSTERING.route('', methods=['GET', 'POST'])
def table():
    """
    Return Main Clustering Page
    """
    today = datetime.now()
    month = today.month - 1
    year = today.year
    if month < 1:
        month = 12
        year = year - 1
    prev_month = datetime(year, month, today.day)

    if request.method == 'GET':
        peminjamans = Peminjaman.get_latest_month_peminjaman()
        clustering = Clustering(prev_month.month, prev_month.year)
        print(clustering.cluster(peminjamans))
    else:
        is_detail = request.form['is_detail']
        clustering_id = request.form['clustering_id']
        cluster_label = request.form['cluster_label']
        clustering = Clustering.find(clustering_id)
        if clustering is not None:
            if is_detail == 'true':
                cluster_dict = request.form['cluster_dict']
                clustering_detail = ClusteringDetail(cluster_label, cluster_dict, clustering.id)
                if clustering_detail.insert():
                    print(f"Berhasil {clustering_id} - {cluster_label} - {cluster_dict}")
                else:
                    print(f"Gagal {clustering_id} - {cluster_label} - {cluster_dict}")
            else:
                clustering_detail = ClusteringDetail.find(cluster_label=cluster_label)
                if clustering_detail is not None:
                    buku_id = request.form['buku_id']
                    peminjaman_clustering = PeminjamanClustering(buku_id, clustering_detail.id)
                    if peminjaman_clustering.insert():
                        print(f"Berhasil {clustering_id} - {buku_id}")
                    else:
                        print(f"Gagal {clustering_id} - {buku_id}")
                else:
                    print(f"Clustering Detail tidak dapat ditemukan")
        else:
            print("Clustering tidak dapat ditemukan")
    return f"{today.year}/{today.month}: {flash_code.SUCCESS}"
