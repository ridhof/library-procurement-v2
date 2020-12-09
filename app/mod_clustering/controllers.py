"""
Clustering Module's Controllers
"""
from flask import Blueprint, request
from datetime import datetime
import pandas as pd
from app.mod_peminjaman.models import Peminjaman
from app.mod_clustering.models import Clustering, ClusteringDetail, PeminjamanClustering

from common import flash_code
from common.fpgrowth import FPGrowth

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
        bulan = prev_month.month
        if len(f"{bulan}") == 1:
            bulan = f"0{bulan}"
        tahun = prev_month.year

        if request.args.get("bulan") and request.args.get("tahun"):
            bulan = request.args.get("bulan")
            tahun = request.args.get("tahun")
        peminjamans = Peminjaman.get_peminjaman(periode=f"{tahun}-{bulan}")
        clustering = Clustering(int(bulan), int(tahun))
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
                clustering_detail = ClusteringDetail.find(cluster_label=cluster_label, clustering_id=clustering_id)
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

@MOD_CLUSTERING.route('<periode>/csv', methods=['GET', 'POST'])
def export_csv(periode):
    """
    Return CSV file
    """
    tahun = int(periode.split('-')[0])
    bulan = int(periode.split('-')[1])

    clustering_id = Clustering.find_id(bulan=bulan, tahun=tahun)
    clusterings = Clustering.find(clustering_id)
    if clusterings is not None:
        tahun = clusterings.tahun
        bulan = clusterings.bulan
        if len(f"{ bulan }") == 1:
            bulan = f"0{ bulan }"
        peminjamans = Peminjaman.get_peminjaman(periode=f"{tahun}-{bulan}")
        peminjaman_dicts = []
        for peminjaman in peminjamans:
            pemustaka = peminjaman.get_pemustaka()
            tanggal_pinjam = peminjaman.get_tanggal()
            buku_id = peminjaman.buku_id
            peminjaman_clustering_id = PeminjamanClustering.get_id(buku_id, clustering_id)
            if peminjaman_clustering_id is not None:
                peminjaman_clustering = PeminjamanClustering.find(peminjaman_clustering_id)
                clustering_detail = ClusteringDetail.find_by_id(peminjaman_clustering.clustering_detail_id)
                peminjaman_dicts.append({
                    'pemustaka': pemustaka,
                    'tanggal_pinjam': tanggal_pinjam,
                    'peminjaman_clustering_id': clustering_detail.cluster_dict
                })
        
        transactions = []
        tanggal_looping = peminjaman_dicts[0]['tanggal_pinjam']
        pemustaka_looping = peminjaman_dicts[0]['pemustaka']
        pemustaka_transaction = []
        for peminjaman in peminjaman_dicts:
            pemustaka = peminjaman['pemustaka']
            tanggal_pinjam = peminjaman['tanggal_pinjam']
            peminjaman_clustering_id = peminjaman['peminjaman_clustering_id']

            if tanggal_pinjam == tanggal_looping and pemustaka == pemustaka_looping:
                if peminjaman_clustering_id not in pemustaka_transaction:
                    pemustaka_transaction.append(peminjaman_clustering_id)
            else:
                transactions.append(pemustaka_transaction)
                tanggal_looping = tanggal_pinjam
                pemustaka_looping = pemustaka
                pemustaka_transaction = [peminjaman_clustering_id]
        transactions.append(pemustaka_transaction)
        
        fpgrowth = FPGrowth(transactions)
        csv_data = []

        title = ['Transaksi']
        title.extend(fpgrowth.transactions_df.columns.to_numpy().tolist())
        index = 1
        for transaction in fpgrowth.transactions_df.to_numpy().tolist():
            row = [f"{index}"]
            for item in transaction:
                value = '?'
                if item == True:
                    value = 'Y'
                row.append(value)
            csv_data.append(row)
            index = index + 1
        csv_df = pd.DataFrame(data=csv_data, columns=title)
        csv_df.to_csv(f"./app/static/files/{periode}.csv", index=False)
        return f"{csv_df}"
    return f"Hello World! {periode}"
