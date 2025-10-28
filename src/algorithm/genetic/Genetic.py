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
        self.verbose = True

        # === Variabel internal ===
        self.population = []
        self.best_state = None
        self.best_value = float("inf")
        self.history = []  # menyimpan objective terbaik per iterasi

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
        if random.random() < self.mutation_rate:
            neighbors = generate_neighbors(state)
            if neighbors:
                return random.choice(neighbors)
        return state

    def run(self):
        print("\n=== Genetic Algorithm ===")
        self.initialize_population()
        start_time = time.time()

        for i in range(self.max_iterasi):
            scored = [(ind, objective_function(ind, self.kapasitas)) for ind in self.population]
            scored.sort(key=lambda x: x[1])
            best_state, best_val = scored[0]
            self.history.append(best_val)

            if best_val < self.best_value:
                self.best_value = best_val
                self.best_state = deepcopy(best_state)

            if self.verbose:
                print(f"Iterasi {i+1} | Objective terbaik: {best_val}")

            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child1, child2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            self.population = new_population[:self.population_size]

        elapsed_time = time.time() - start_time

        print("\n=== Hasil Akhir ===")
        print(self.best_state)
        print(f"Nilai Objective Terbaik : {self.best_value}")
        print(f"Jumlah Iterasi          : {self.max_iterasi}")
        print(f"Jumlah Populasi         : {self.population_size}")
        print(f"Probabilitas Mutasi     : {self.mutation_rate}")
        print(f"Waktu Eksekusi          : {elapsed_time:.2f} detik")

        self.show_plot()
        return self.best_state, self.best_value, elapsed_time

    def show_plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.history, color="green", marker="o", linewidth=2)
        plt.title("Perkembangan Nilai Objective Function per Iterasi")
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function (semakin kecil semakin baik)")
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.tight_layout()
        plt.show()
