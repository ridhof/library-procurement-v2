"""
Clustering's Tasks
"""
import requests
from common.vectorize import Vectorize
from common.clustering import Clustering
from common import config


def do_clustering(clustering_id, peminjamans, url):
    juduls = []
    distinct_peminjamans = []
    for peminjaman in peminjamans:
        if peminjaman['buku_title'] not in juduls:
            juduls.append(peminjaman['buku_title'])
            distinct_peminjamans.append(peminjaman)
    vectorize = Vectorize(juduls)
    clustering = Clustering(datas=vectorize.vectors, features=vectorize.features, is_scale=True)
    print(clustering)
    
    peminjaman_by_cluster = {}
    for label in clustering.labels:
        peminjaman_by_cluster[label] = []
    print(peminjaman_by_cluster)

    for peminjaman_idx in range(len(distinct_peminjamans)):
        label = clustering.labels[peminjaman_idx]
        distinct_peminjamans[peminjaman_idx]['label'] = label
        peminjaman_by_cluster[label].append(distinct_peminjamans[peminjaman_idx])
    print(peminjaman_by_cluster)
        
    for cluster in peminjaman_by_cluster:
        payload = {
            'is_detail': 'true',
            'clustering_id': clustering_id,
            'cluster_label': cluster,
            'cluster_dict': clustering.dicts[cluster]
        }
        r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
        print(f"{r.status_code}: {r.text}")
        for peminjaman in peminjaman_by_cluster[cluster]:
            payload = {
                'is_detail': 'false',
                'clustering_id': clustering_id,
                'cluster_label': cluster,
                'buku_id': peminjaman['buku_id']
            }
            r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
            print(f"{r.status_code}: {r.text}")

    fpgrowth_request = requests.get(f"{config.SERVER_URL}/fpgrowth/?clustering_id={clustering_id}")
    print(f"FPGrowth Request {fpgrowth_request.status_code}: {fpgrowth_request.text}")
