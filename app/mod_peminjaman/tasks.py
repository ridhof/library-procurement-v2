"""
Peminjaman's Tasks
"""
import os
import requests
from common.excel import Excel
from common import config


def read_excel(path, sheet_index, url):
    excel = Excel(path, sheet_index)
    excel.store(f"{url}")

    if os.path.exists(path):
        os.remove(path)

    print(f"Proses impor data peminjaman dari excel, selesai")
