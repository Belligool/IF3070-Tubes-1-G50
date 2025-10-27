# Insialisasi kelas Barang dengan atribut id dan ukuran

class Barang:
    def __init__(self, id_barang, ukuran):
        self.id = id_barang
        self.ukuran = ukuran

    def __repr__(self):
        return f"{self.id} ({self.ukuran})"
