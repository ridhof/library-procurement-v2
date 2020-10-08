"""
Perceptron Class
"""
from app import DB as db, REDIS as redis, REDIS_QUEUE as rqueue
from app.models import Base
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
