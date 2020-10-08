"""
Perceptron's Tasks
"""
import requests
from common.prioriceptron import Prioriceptron
from common import config

def do_perceptron(peminjamans, url):
    print(f"Running Perceptron Process using {len(peminjamans)} data")
    transactions = []

    tanggal_looping = peminjamans[0]['tanggal_pinjam']
    cluster_looping = peminjamans[0]['peminjaman_clustering_id']
    cluster_transaction = []

    print("Looping on Peminjaman")
    for peminjaman in peminjamans:
        tanggal_pinjam = peminjaman['tanggal_pinjam']
        cluster_id = peminjaman['peminjaman_clustering_id']

        if tanggal_pinjam == tanggal_looping:
            cluster_transaction.append(f"{cluster_id}")
        else:
            transactions.append(" ".join(cluster_transaction))

            tanggal_looping = tanggal_pinjam
            cluster_transaction = [f"{cluster_id}"]
    transactions.append(" ".join(cluster_transaction))
    print(f"{len(transactions)} day of transactions achieved")

    print("Calculating Priorities using Perceptron")
    prioriceptron = Prioriceptron(transactions)
    print("Perceptron Result Retrieved")

    print("Looping Perceptron Result")
    for priority in prioriceptron.priorities:
        print(f"Sending the Looped Priorty to Endpoint, {priority}")
        payload = priority
        r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
        print(f"{r.status_code}: {r.text}")
    
