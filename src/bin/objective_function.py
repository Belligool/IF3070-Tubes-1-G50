def objective_function(state, kapasitas):
    total_penalty = 0

    for current_kontainer in state.kontainer_list:
        total_isi = sum(b.ukuran for b in current_kontainer.isi)

        if total_isi > kapasitas:
            total_penalty += 1000 * (total_isi - kapasitas)
        else:
            total_penalty += (kapasitas - total_isi)

    total_penalty += len(state.kontainer_list) * 10

    return total_penalty
