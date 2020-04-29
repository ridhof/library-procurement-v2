"""
RPS's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common import config


def preprocess_rps(kompetensi, indikator, materi, url):
    preprocessed_kompetensi = NLP(kompetensi)
    preprocessed_indikator = NLP(indikator)
    preprocessed_materi = NLP(materi)

    payload = {
        'preprocessed_kompetensi': preprocessed_kompetensi.preprocessed_text,
        'preprocessed_indikator': preprocessed_indikator.preprocessed_text,
        'preprocessed_materi': preprocessed_materi.preprocessed_text
    }

    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}")
