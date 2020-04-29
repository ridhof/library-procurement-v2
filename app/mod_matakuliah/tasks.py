"""
Matakuliah's Tasks
"""
import requests
from common.nlp_preprocess import NLP
from common import config

def preprocess_matakuliah(deskripsi_singkat, standar_kompetensi, url):
    preprocessed_deskripsi = NLP(deskripsi_singkat)
    preprocessed_standar = NLP(standar_kompetensi)

    payload = {
        'preprocessed_deskripsi': preprocessed_deskripsi.preprocessed_text,
        'preprocessed_standar': preprocessed_standar.preprocessed_text
    }
    r = requests.post(f"{config.SERVER_URL}{url}", data=payload)
    print(f"{r.status_code}: {r.text}") 
