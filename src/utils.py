import os
import json
from bin.entity.barang import Barang

def load_input(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        file_path = os.path.join(base_dir, filename)
        print(f"\nMembaca file dari: {file_path}")

        # Cek apakah file ada
        if not os.path.exists(file_path):
            print("ERROR: File tidak ditemukan!")
            filename = input("Masukkan ulang nama file input (contoh: input.json): ")
            continue

        # Coba buka file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("ERROR: Format JSON tidak valid!")
            filename = input("Masukkan ulang nama file input (contoh: input.json): ")
            continue

        # Validasi struktur file JSON
        try:
            kapasitas = data["kapasitas_kontainer"]
            barang_list = [Barang(item["id"], item["ukuran"]) for item in data["barang"]]
        except KeyError:
            print("ERROR: Struktur JSON salah!")
            print("   Wajib ada 'kapasitas_kontainer' dan 'barang'")
            filename = input("Masukkan ulang nama file input (contoh: input.json): ")
            continue

        print("File input berhasil dibaca!\n")
        return kapasitas, barang_list


def print_centered_header(text): #dekorasi aja
    """Print text with center alignment"""
    lines = text.strip().split('\n')
    for line in lines:
        print(line.center(80))  
