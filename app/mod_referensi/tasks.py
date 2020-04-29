"""
Referensi's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common import config


def preprocess_referensi(pengarang, judul, url):
    preprocessed_keterangan = NLP(f"{pengarang} {judul}")

    payload = {
        'preprocessed_keterangan': preprocessed_keterangan.preprocessed_text
    }

    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}")
