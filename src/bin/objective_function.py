def objective_function(state, kapasitas):
    total_penalty = 0

    for current_kontainer in state.kontainer_list:
        total_isi = sum(barang.ukuran for barang in current_kontainer.isi)

        if total_isi > kapasitas: 
            total_penalty += 1000 * (total_isi - kapasitas) # penalti over capacity
        else:
            total_penalty += (kapasitas - total_isi) # penalti ruang kosong

    total_penalty += len(state.kontainer_list) * 10 # penalti jumlah kontainer

    return total_penalty
