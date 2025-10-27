def generate_neighbors(state):
    """
        Membuat semua possible neighbor dari state sekarang
        dengan cara memindahkan satu barang dari satu kontainer
        ke kontainer lain (atau ke kontainer baru).
    """
    neighbors = []
    kontainer_list = state.kontainer_list

    for i, src in enumerate(kontainer_list):
        for barang in src.isi[:]: 

            for j, dest in enumerate(kontainer_list):
                if i == j:
                    continue  

                new_state = state.clone()
                new_src = new_state.kontainer_list[i]
                new_dest = new_state.kontainer_list[j]

                new_src.hapus_barang(barang)
                if new_dest.tambah_barang(barang):
                    # valid move
                    neighbors.append(new_state)
                else:
                    # rollback saat tidak muat
                    new_src.tambah_barang(barang)

            new_state = state.clone()
            new_src = new_state.kontainer_list[i]
            new_src.hapus_barang(barang)

            from bin.entity.kontainer import Kontainer
            new_container = Kontainer(state.kontainer_list[0].kapasitas)
            new_container.tambah_barang(barang)
            new_state.kontainer_list.append(new_container)
            neighbors.append(new_state)

    return neighbors
