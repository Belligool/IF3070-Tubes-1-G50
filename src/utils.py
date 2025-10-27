import os
import json
from bin.entity.barang import Barang

def load_input(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    print(f"Membaca file dari: {file_path}") 

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    kapasitas = data["kapasitas_kontainer"]
    barang_list = [Barang(item["id"], item["ukuran"]) for item in data["barang"]]
    return kapasitas, barang_list

def print_centered_header(text): #dekorasi aja
    """Print text with center alignment"""
    lines = text.strip().split('\n')
    for line in lines:
        print(line.center(80))  
