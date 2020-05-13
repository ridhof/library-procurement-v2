PINJAM = 'pinjam'
KEMBALI = 'kembali'
PERPANJANG = 'perpanjang'


def get_status():
    list_status = [
        (PINJAM, PINJAM.capitalize()),
        (KEMBALI, KEMBALI.capitalize()),
        (PERPANJANG, PERPANJANG.capitalize())
    ]
    return list_status