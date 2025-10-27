from .barang import Barang

class Kontainer:
    def __init__(self, kapasitas):
        self.kapasitas = kapasitas
        self.isi = []

    # Fungsi untuk menambahkan barang ke dalam kontainer
    def tambah_barang(self, barang):
        if not isinstance(barang, Barang):
            raise TypeError("Hanya objek dari class Barang yang bisa dimasukkan ke dalam Kontainer.")

        if self.total_isi() + barang.ukuran <= self.kapasitas:
            self.isi.append(barang)
            return True
        return False

    # Fungsi untuk menghapus barang dari kontainer
    def hapus_barang(self, barang):
        if barang in self.isi:
            self.isi.remove(barang)

    # Fungsi untuk menghitung total ukuran barang dalam kontainer
    def total_isi(self):
        return sum(b.ukuran for b in self.isi)

    # Fungsi representasi string dari kontainer
    def __repr__(self):
        return f"Kontainer(total: {self.total_isi()}/{self.kapasitas}, isi: {self.isi})"
