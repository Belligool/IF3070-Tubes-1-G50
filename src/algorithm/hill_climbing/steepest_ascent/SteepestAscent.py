import matplotlib.pyplot as plt
import time
from bin.objective_function import objective_function
from bin.neighbor_state import generate_neighbors

class SteepestAscent:
    def __init__(self, initial_state, kapasitas):
        self.current_state = initial_state
        self.kapasitas = kapasitas
        self.current_value = objective_function(initial_state, kapasitas)
        self.objective_values = [self.current_value]

    def search_best_neighbor(self):
        best_neighbor = None
        best_value = self.current_value

        neighbors = generate_neighbors(self.current_state)
        for neighbor in neighbors:
            value = objective_function(neighbor, self.kapasitas)
            if value < best_value:
                best_value = value
                best_neighbor = neighbor
        return best_neighbor, best_value

    def run(self):
        total_iteration = 0

        print("\n==============================")
        print("STATE AWAL STEEPEST ASCENT")
        print("==============================")
        print(self.current_state)
        print(f"Objective awal: {self.current_value}")
        print(f"Total Kontainer: {len(self.current_state.kontainer_list)}\n")

        start_time = time.time()

        while True:
            best_neighbor, best_value = self.search_best_neighbor()

            if best_neighbor is not None and best_value < self.current_value:
                self.current_state = best_neighbor
                self.current_value = best_value
                total_iteration += 1
                self.objective_values.append(self.current_value)

                print(
                    f"Iterasi {total_iteration} → Objective: {self.current_value} "
                    f"(Kontainer: {len(self.current_state.kontainer_list)})"
                )
            else:
                break

        elapsed_time = time.time() - start_time

        print("\n==============================")
        print("  STATE AKHIR STEEPEST ASCENT   ")
        print("================================")
        print(self.current_state)
        print(f"Nilai Objective Akhir : {self.current_value}")
        print(f"Total Kontainer       : {len(self.current_state.kontainer_list)}")
        print(f"Total Iterasi         : {total_iteration}")
        print(f"Waktu Eksekusi        : {elapsed_time:.3f} detik\n")

        self.show_plot(self.objective_values,
            title=f"Perkembangan Nilai Objective Function\n(Waktu: {elapsed_time:.2f} detik)"
        )
        return self.current_state, self.current_value, elapsed_time

    @staticmethod
    def show_plot(objective_values, title="Perkembangan Objective Value per Iterasi"):
        if len(objective_values) < 2:
            print("Tidak cukup data untuk menampilkan grafik (solusi tidak membaik).")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(
            range(len(objective_values)),
            objective_values,
            label="Objective Value",
            color="blue",
            linewidth=2,
            marker='o'
        )
        plt.title(title)
        plt.xlabel("Iteration")
        plt.ylabel("Objective Value")
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()
