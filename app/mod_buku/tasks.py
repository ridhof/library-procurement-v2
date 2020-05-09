"""
Buku's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common import config


def preprocess_judul(judul, url):
    preprocessed_judul = NLP(judul)

    payload = {
        'preprocessed_judul': preprocessed_judul.preprocessed_text
    }

    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}")
