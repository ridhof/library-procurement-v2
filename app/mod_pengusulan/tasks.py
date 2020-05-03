"""
Pengusulan's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common.similarity import Similarity
from common import config


def preprocess_pengusulan(judul, url):
    preprocessed_judul = NLP(judul)

    payload = {
        'preprocessed_judul': preprocessed_judul.preprocessed_text
    }

    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}")

def count_similarity(fact, queries, urls):
    print("Doing similarity processing")
    similarity = Similarity(fact, queries)

    for score_idx in range(len(similarity.scores)):
        print("Storing Scores")
        score = similarity.scores[score_idx]
        payload = {
            'score': score
        }

        r = requests.post(f"{config.SERVER_URL}{urls[score_idx]}", data=payload)
        print(f"{r.status_code}: {r.text}")
