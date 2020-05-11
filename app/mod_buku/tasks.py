"""
Buku's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common.similarity import Similarity
from common import config


def preprocess_judul(judul, queries_text, queries_id, url):
    preprocessed_judul = NLP(judul)
    similarity = Similarity(
        fact=preprocessed_judul.preprocessed_text, 
        queries=queries_text
    )

    max_score_id = similarity.scores.index(max(similarity.scores))
    dewey_id = queries_id[max_score_id]

    payload = {
        'preprocessed_judul': preprocessed_judul.preprocessed_text,
        'dewey_id': dewey_id
    }

    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}")
