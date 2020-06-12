"""
Clustering Class
"""
from flask import url_for
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.models import Base
from app.mod_clustering.tasks import do_clustering
from common import flash_code, peminjaman_code


class Clustering(Base):

    __tablename__ = 'clustering'

    bulan = db.Column(db.Integer, nullable=True)
    tahun = db.Column(db.Integer, nullable=True)

    def __init__(self, bulan, tahun):
        self.bulan = bulan
        self.tahun = tahun

    def __repr__(self):
        return '<Clustering %r>' % (self.id)

    def cluster(self, peminjamans):
        try:
            peminjaman_process = []
            for peminjaman in peminjamans:
                if peminjaman.status != peminjaman_code.KEMBALI:
                    peminjaman_process.append({
                        'peminjaman_id': peminjaman.id,
                        'tanggal_pinjam': peminjaman.get_tanggal(),
                        'buku_id': peminjaman.buku_id,
                        'buku_title': peminjaman.get_buku(is_preprocessed=True),
                        'peminjam': peminjaman.get_pemustaka()
                    })
            db.session.add(self)
            db.session.commit()
            task = rqueue.enqueue(
                do_clustering,
                self.id,
                peminjaman_process,
                url_for('clustering.table')
            )
            return True
        except:
            return False

    def find(clustering_id):
        return Clustering.query.filter_by(id=clustering_id, is_delete=0).first()

    def find_id(bulan, tahun):
        clustering = Clustering.query.filter_by(bulan=bulan, tahun=tahun, is_delete=0).first()
        return clustering.id

class ClusteringDetail(Base):

    __tablename__ = 'clustering_detail'

    cluster_label = db.Column(db.Integer, nullable=True)
    cluster_dict = db.Column(db.String(60), nullable=True)

    clustering_id = db.Column(db.Integer, nullable=False)

    def __init__(self, cluster_label, cluster_dict, clustering_id):
        self.cluster_label = cluster_label
        self.cluster_dict = cluster_dict
        self.clustering_id = clustering_id

    def __repr__(self):
        return '<ClusteringDetail %r>' % (self.id)

    def find_by_id(clustering_detail_id):
        return ClusteringDetail.query.filter_by(id=clustering_detail_id, is_delete=0).first()

    def find(cluster_label, clustering_id):
        return ClusteringDetail.query.filter_by(cluster_label=cluster_label, clustering_id=clustering_id, is_delete=0).first()
    
    def get_details(clustering_id):
        return ClusteringDetail.query.filter_by(clustering_id=clustering_id, is_delete=0).all()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


class PeminjamanClustering(Base):
    
    __tablename__ = 'peminjaman_clustering'

    buku_id = db.Column(db.Integer, nullable=False)
    clustering_detail_id = db.Column(db.Integer, nullable=False)

    def __init__(self, buku_id, clustering_detail_id):
        self.buku_id = buku_id
        self.clustering_detail_id = clustering_detail_id

    def __repr__(self):
        return '<PeminjamanClustering %r>' % (self.id)

    def find(id):
        return PeminjamanClustering.query.filter_by(id=id, is_delete=0).first()

    def get_id(buku_id, clustering_id):
        try:
            peminjaman_clusterings = PeminjamanClustering.query.filter_by(buku_id=buku_id, is_delete=0).all()
            peminjaman_clustering_id = None
            for peminjaman_clustering in peminjaman_clusterings:
                clustering_detail = ClusteringDetail.query.filter_by(id=peminjaman_clustering.clustering_detail_id, is_delete=0).first()
                if clustering_detail.clustering_id == int(clustering_id):
                    peminjaman_clustering_id = peminjaman_clustering.id
            return peminjaman_clustering_id
        except Exception:
            return None
    
    def get_by_detail(clustering_detail_id):
        return PeminjamanClustering.query.filter_by(clustering_detail_id=clustering_detail_id, is_delete=0).all()

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
