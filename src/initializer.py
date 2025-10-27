from bin.entity.kontainer import Kontainer
from bin.state import State

def generate_initial_state(barang_list, kapasitas):
    """
    Generate initial state dengan First Fit Decreasing (FFD) heuristic.
    """
    kontainer_list = [Kontainer(kapasitas)]
    for barang in barang_list:
        placed = False
        for k in kontainer_list:
            if k.tambah_barang(barang):
                placed = True
                break
        if not placed:
            new_k = Kontainer(kapasitas)
            new_k.tambah_barang(barang)
            kontainer_list.append(new_k)

    return State(kontainer_list)