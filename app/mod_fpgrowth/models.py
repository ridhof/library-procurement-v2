"""
FPGrowth Class
"""
from flask import url_for
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.models import Base
from app.mod_clustering.models import Clustering, ClusteringDetail, PeminjamanClustering
from app.mod_fpgrowth.tasks import do_fpgrowth

from common import flash_code


class FrequentPatternGrowth(Base):

    __tablename__ = 'fpgrowth'

    confidence_value = db.Column(db.Float, nullable=True)
    support_value = db.Column(db.Float, nullable=True)
    lift_value = db.Column(db.Float, nullable=True)

    main_itemset = db.Column(db.Integer, nullable=False)
    correlated_itemset = db.Column(db.Integer, nullable=False)

    def __init__(self, confidence_value, support_value, lift_value, main_itemset, correlated_itemset):
        self.confidence_value = confidence_value
        self.support_value = support_value
        self.lift_value = lift_value
        self.main_itemset = main_itemset
        self.correlated_itemset = correlated_itemset

    def __repr__(self):
        return '<FPGrowth %r>' % (self.id)

    def get(periode):
        try:
            tahun = int(periode.split('-')[0])
            bulan = int(periode.split('-')[1])
            clustering_id = Clustering.find_id(bulan, tahun)
            if clustering_id is not None:
                clustering_details = ClusteringDetail.get_details(
                    clustering_id)
                if clustering_details is not None:
                    peminjaman_clusterings = []
                    for detail in clustering_details:
                        peminjaman_clustering = PeminjamanClustering.get_by_detail(
                            detail.id)
                        peminjaman_clusterings.extend(peminjaman_clustering)

                    fpgrowths = []
                    for peminjaman in peminjaman_clusterings:
                        fpgrowth = FrequentPatternGrowth.query.filter_by(
                            main_itemset=peminjaman.id, is_delete=0).all()
                        fpgrowths.extend(fpgrowth)
                    return fpgrowths

            return []
        except:
            return []

    def get_cluster_dict(self, peminjaman_clustering_id):
        result = peminjaman_clustering_id
        peminjaman_clustering = PeminjamanClustering.find(peminjaman_clustering_id)
        if peminjaman_clustering is not None:
            clustering_detail = ClusteringDetail.find_by_id(peminjaman_clustering.clustering_detail_id)
            if clustering_detail is not None:
                result = clustering_detail.cluster_dict
        return result

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def helper(peminjamans):
        try:
            task = rqueue.enqueue(
                do_fpgrowth,
                peminjamans,
                '/fpgrowth/'
            )
            return True
        except:
            return False
