from copy import deepcopy
import matplotlib.pyplot as plt
import time, random
from bin.objective_function import objective_function
from bin.neighbor_state import generate_neighbors


class GeneticAlgorithm:
    def __init__(self, initial_state, kapasitas):
        """
        Genetic Algorithm untuk optimisasi penempatan barang ke kontainer.
        Parameter utama (population_size, max_iterasi, mutation_rate)
        akan diminta sebagai input dari user.
        """
        self.initial_state = initial_state
        self.kapasitas = kapasitas

        print("\n=== Input Parameter Genetic Algorithm ===")
        self.population_size = int(input("Masukkan jumlah populasi: "))
        self.max_iterasi = int(input("Masukkan banyak iterasi (generasi): "))
        self.mutation_rate = float(input("Masukkan probabilitas mutasi (contoh: 0.1): "))

        # === Variabel internal ===
        self.population = []
        self.best_state = None
        self.best_value = float("inf")
        self.best_history = [] # objective terbaik tiap iterasi
        self.avg_history = [] # rata-rata objective tiap iterasi
        self.history = []  # catatan nilai objective tiap iterasi

    def initialize_population(self):
        self.population = [deepcopy(self.initial_state)]
        while len(self.population) < self.population_size:
            neighbors = generate_neighbors(self.initial_state)
            if neighbors:
                self.population.append(random.choice(neighbors))
            else:
                break

    def fitness(self, state):
        obj_value = objective_function(state, self.kapasitas)
        return 1 / (1 + obj_value)

    def select_parent(self):
        fitness_values = [self.fitness(ind) for ind in self.population]
        total_fit = sum(fitness_values)
        pick = random.uniform(0, total_fit)
        current = 0
        for i, f in enumerate(fitness_values):
            current += f
            if current >= pick:
                return deepcopy(self.population[i])

    def crossover(self, parent1, parent2):
        child1, child2 = deepcopy(parent1), deepcopy(parent2)
        min_len = min(len(parent1.kontainer_list), len(parent2.kontainer_list))
        if min_len > 1:
            point = random.randint(1, min_len - 1)
            child1.kontainer_list[:point], child2.kontainer_list[:point] = (
                deepcopy(parent2.kontainer_list[:point]),
                deepcopy(parent1.kontainer_list[:point])
            )
        return child1, child2

    def mutate(self, state):
        if random.random() > self.mutation_rate:
            return state   # tidak terjadi mutasi

        new_state = deepcopy(state)
        kontainer_list = new_state.kontainer_list

        # pilih barang acak
        # cari kontainer sumber yang tidak kosong
        sumber = random.choice([k for k in kontainer_list if k.isi])

        barang = random.choice(sumber.isi)

        mutation_type = random.randint(1,3)

        # ========== 1. Pindahkan barang ke kontainer lain ==============
        if mutation_type == 1:
            tujuan = random.choice(kontainer_list)
            if tujuan != sumber:
                sumber.hapus_barang(barang)
                if not tujuan.tambah_barang(barang):
                    sumber.tambah_barang(barang)

        # ======= 2. Tukar barang antar dua kontainer ==================
        elif mutation_type == 2:
            kontainer_lain = random.choice([k for k in kontainer_list if k != sumber and k.isi])
            barang_lain = random.choice(kontainer_lain.isi)

            # swap
            sumber.hapus_barang(barang)
            kontainer_lain.hapus_barang(barang_lain)

            # coba tukar
            if sumber.tambah_barang(barang_lain) and kontainer_lain.tambah_barang(barang):
                pass
            else:
                sumber.tambah_barang(barang)
                kontainer_lain.tambah_barang(barang_lain)

        # =========== 3. Pindahkan ke kontainer baru ====================
        elif mutation_type == 3:
            from bin.entity.kontainer import Kontainer
            sumber.hapus_barang(barang)
            kontainer_baru = Kontainer(self.kapasitas)
            kontainer_baru.tambah_barang(barang)
            kontainer_list.append(kontainer_baru)

        # hapus kontainer kosong
        for k in kontainer_list[:]:
            if len(k.isi) == 0:
                kontainer_list.remove(k)

        return new_state

    def run(self):
        print("\n==============================")
        print("      GENETIC ALGORITHM         ")
        print("================================")

        self.initialize_population()
        start_time = time.time()

        for i in range(self.max_iterasi):
            scored = [(ind, objective_function(ind, self.kapasitas)) for ind in self.population]
            scored.sort(key=lambda x: x[1])  # urutkan dari yang terbaik (penalti plg kecil)

            # Nilai terbaik dan rata-rata
            best_val = scored[0][1]
            avg_val = sum(val for _, val in scored) / len(scored)

            # Simpan ke history
            self.best_history.append(best_val)
            self.avg_history.append(avg_val)

            # Update state terbaik global
            if best_val < self.best_value:
                self.best_value = best_val
                self.best_state = deepcopy(scored[0][0])

            print(f"Iterasi {i+1} | Best: {best_val} | Avg: {avg_val}")

            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            self.population = new_population[:self.population_size]

        elapsed_time = time.time() - start_time

        print("\n========= HASIL AKHIR =========")
        print("State terbaik:")
        print(self.best_state)
        print("\nDetail Eksekusi:")
        print(f"{'Objective Terbaik':25s}: {self.best_value}")
        print(f"{'Jumlah Iterasi':25s}: {self.max_iterasi}")
        print(f"{'Jumlah Populasi':25s}: {self.population_size}")
        print(f"{'Probabilitas Mutasi':25s}: {self.mutation_rate}")
        print(f"{'Waktu Eksekusi':25s}: {elapsed_time:.4f} detik")
        print("=" * 32)

        self.show_plot()
        return self.best_state, self.best_value, elapsed_time

    def show_plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.best_history, marker="o", label="Nilai Objective Terbaik (Min)")
        plt.plot(self.avg_history, marker="x", label="Rata-rata Objective per Iterasi")
        plt.title("Perkembangan Objective Function per Iterasi")
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function (Penalti)")
        plt.legend()
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.tight_layout()
        plt.show()
