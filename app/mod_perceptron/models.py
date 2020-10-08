"""
Perceptron Class
"""
import operator
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.models import Base
from app.mod_clustering.models import Clustering, ClusteringDetail, PeminjamanClustering
from app.mod_perceptron.tasks import do_perceptron

class Perceptron(Base):

    __tablename__ = 'perceptron'

    cluster_id = db.Column(db.Integer, nullable=False)
    priority_value = db.Column(db.Float, nullable=True)

    def __init__(self, cluster_id, priority_value):
        self.cluster_id = cluster_id
        self.priority_value = priority_value

    def __repr__(self):
        return '<Perceptron %r>' % (self.id)

    def get(periode):
        try:
            tahun = int(periode.split('-')[0])
            bulan = int(periode.split('-')[1])
            clustering_id = Clustering.find_id(bulan, tahun)
            if clustering_id is not None:
                clustering_details = ClusteringDetail.get_details(clustering_id)
                if clustering_details is not None:
                    perceptrons = []
                    for detail in clustering_details:
                        perceptron = Perceptron.query.filter_by(cluster_id=detail.id, is_delete=0).all()
                        perceptrons.extend(perceptron)

                    perceptrons_result_sorted = sorted(perceptrons, key=operator.attrgetter('priority_value'), reverse=True)
                    [print(f"Topik {perceptron.cluster_id} has priority {perceptron.priority_value}") for perceptron in perceptrons_result_sorted]
                    return perceptrons_result_sorted
            return []
        except:
            return []

    def get_cluster_dict(self, clustering_detail_id, is_display=False):
        result = clustering_detail_id
        clustering_detail = ClusteringDetail.find_by_id(clustering_detail_id)
        if clustering_detail is not None:
            result = clustering_detail.cluster_dict
            if is_display:
                array_dict = result.split('-')
                result = f"{array_dict[1]} {array_dict[0]}".title()
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
                do_perceptron,
                peminjamans,
                '/perceptron/'
            )
            return True
        except:
            return False
