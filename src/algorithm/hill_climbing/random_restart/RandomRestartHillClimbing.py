import time
import random
import matplotlib.pyplot as plt
from bin.objective_function import objective_function as evaluate
from bin.neighbor_state import generate_neighbors
from initializer import generate_initial_state

class RandomRestartHillClimbing:
    def __init__(self, barang_list, kapasitas):
        self.barang_list_master = barang_list
        self.kapasitas = kapasitas
        self.max_restarts = 0

        self.global_best_state = None
        self.global_best_eval = float("inf")
        
        self.scores_history = [] 
        self.iterations_per_restart = []

    def _plot_scores(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.scores_history)
        plt.title("Best Score vs. Total Iterations (Random Restart)")
        plt.xlabel("Total Iterations (in all restarts)")
        plt.ylabel("Global Best Score")
        plt.grid(True)
        print("Menampilkan Plot Skor...")
        plt.show()

    def _run_local_search(self, start_state):
        current_state = start_state
        current_eval = evaluate(current_state, self.kapasitas)
        iter_count = 0
        
        print(f"  ... Memulai local search dari skor: {current_eval:.2f}")
        
        while True:
            neighbors = generate_neighbors(current_state)
            if not neighbors:
                break

            best_neighbor = None
            best_neighbor_eval = current_eval

            for neighbor in neighbors:
                eval_n = evaluate(neighbor, self.kapasitas)
                if eval_n < best_neighbor_eval:
                    best_neighbor_eval = eval_n
                    best_neighbor = neighbor

            if best_neighbor_eval < current_eval:
                current_state = best_neighbor
                current_eval = best_neighbor_eval
                iter_count += 1
                
                if current_eval < self.global_best_eval:
                    self.global_best_eval = current_eval
                    self.global_best_state = current_state
                print(f"  ... Iterasi {iter_count}: Current {current_eval:.2f}, Global Best {self.global_best_eval:.2f}  ", end='\r')

            else:
                break
            
            self.scores_history.append(self.global_best_eval)

        print()
        return current_state, current_eval, iter_count

    def run(self):
        try:
            max_restarts_input = int(input("Masukkan Max Restarts (misal: 10): "))
        except ValueError:
            print("Error: Input harus angka. Menggunakan default 10.")
            max_restarts_input = 10
        
        self.max_restarts = max_restarts_input
        
        print(f"--- Memulai Random Restart Hill Climbing (Max Restarts: {self.max_restarts}) ---")
        start_time = time.time()
        
        self.scores_history = []

        for r in range(self.max_restarts):
            print(f"\n--- Restart {r + 1}/{self.max_restarts} ---")
            
            shuffled_list = self.barang_list_master[:]
            random.shuffle(shuffled_list)
            initial_state = generate_initial_state(shuffled_list, self.kapasitas)
            
            initial_eval = evaluate(initial_state, self.kapasitas)
            
            if initial_eval < self.global_best_eval:
                self.global_best_eval = initial_eval
                self.global_best_state = initial_state
            
            self.scores_history.append(self.global_best_eval)
            
            if r == 0:
                print("State Awal (dari Restart 1):")
                print(initial_state)
                print(f"Skor Awal: {initial_eval:.2f}")

            local_best_state, local_best_eval, iter_count = self._run_local_search(initial_state)
            
            print(f"Restart {r + 1} selesai setelah {iter_count} iterasi. Local Best: {local_best_eval:.2f}, Global Best: {self.global_best_eval:.2f}")
            self.iterations_per_restart.append(iter_count)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n--- Random Restart Hill Climbing Selesai ---")
        print(f"Durasi Total: {duration:.4f} detik")
        print(f"Total Iterasi (di semua restart): {len(self.scores_history) - self.max_restarts}")
        print(f"Best Score Ditemukan: {self.global_best_eval}")
        if self.iterations_per_restart:
            print(f"Rata-rata iterasi per restart: {sum(self.iterations_per_restart) / len(self.iterations_per_restart):.2f}")

        print("\n--- STATE AKHIR (HASIL GLOBAL TERBAIK) ---")
        if self.global_best_state:
            print(self.global_best_state)
            print(f"Total Kontainer: {self.global_best_state.total_kontainer()}")
            print(f"Skor Akhir Terbaik: {self.global_best_eval}")
        else:
            print("Tidak ada solusi yang ditemukan")
        print("------------------------------\n")
        
        print("Menyiapkan plot...")
        print("(Tutup window plot untuk melanjutkan program)")
        self._plot_scores()

        return