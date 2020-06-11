"""
FPGrowth's Tasks
"""
import requests
from common.fpgrowth import FPGrowth
from common import config


def do_fpgrowth(peminjamans, url):
    transactions = []

    tanggal_looping = peminjamans[0]['tanggal_pinjam']
    pemustaka_looping = peminjamans[0]['pemustaka']
    pemustaka_transaction = []
    for peminjaman in peminjamans:
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
    for rule in fpgrowth.association_rules:
        # print(rule)
        payload = rule
        r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
        print(f"{r.status_code}: {r.text}")
