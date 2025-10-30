import time
import matplotlib.pyplot as plt
from bin.objective_function import objective_function as evaluate
from bin.neighbor_state import generate_neighbors

class HillClimbingSideways:
    def __init__(self, initial_state, kapasitas):
        self.kapasitas = kapasitas

        self.current_state = initial_state
        self.current_eval = evaluate(self.current_state, self.kapasitas)

        self.best_state = initial_state
        self.best_eval = self.current_eval
        self.scores_history = [self.best_eval]

    def _plot_scores(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.scores_history)
        plt.title("Score vs Iteration (Hill Climbing w/ Sideways Move)")
        plt.xlabel("Iteration")
        plt.ylabel("Best Score")
        plt.grid(True)
        print("Menampilkan Plot Skor...")
        plt.show()
    
    def run(self):
        print("\n--- STATE AWAL ---")
        print(self.current_state)
        print(f"Skor Awal: {self.current_eval}")
        print("-----------------------\n")

        max_sideways_moves = int(input("Masukkan Max Sideways Moves (misal: 10): "))
            
        print("--- Memulai Hill Climbing w/ Sideways Move ---")
        start_time = time.time()
        sideways_move_count = 0
        iteration = 0

        while True:
            neighbors = generate_neighbors(self.current_state)

            if not neighbors:
                print("Tidak ada tetangga yang bisa digenerate. Berhenti.")
                break
            
            best_neighbor = None
            best_neighbor_eval = float("inf")

            for neighbor in neighbors:
                eval_n = evaluate(neighbor, self.kapasitas)
                if eval_n < best_neighbor_eval:
                    best_neighbor_eval = eval_n
                    best_neighbor = neighbor
            
            self.current_eval = evaluate(self.current_state, self.kapasitas)
            
            if best_neighbor_eval < self.current_eval:
                self.current_state = best_neighbor
                sideways_move_count = 0

                if best_neighbor_eval < self.best_eval:
                    self.best_eval = best_neighbor_eval
                    self.best_state = best_neighbor
            
            elif best_neighbor_eval == self.current_eval:
                if sideways_move_count >= max_sideways_moves:
                    print(f"\nBatas maksimum {max_sideways_moves} sideways move tercapai. Berhenti.")
                    break
                else:
                    self.current_state = best_neighbor
                    sideways_move_count += 1
            
            else:
                print("\nTidak ada langkah yang lebih baik atau sideways. Terjebak di local optimum.")
                break

            self.scores_history.append(self.best_eval)
            print(f"Iter: {iteration}, Best: {self.best_eval:.2f}, Current: {evaluate(self.current_state, self.kapasitas):.2f}, Sideways: {sideways_move_count}/{max_sideways_moves}")
            iteration += 1
        
        end_time = time.time()
        duration = end_time - start_time

        print("--- Hill Climbing w/ Sideways Move Selesai ---")
        print(f"Durasi: {duration:.4f} detik")
        print(f"Berhenti setelah {iteration} iterasi")
        print(f"Best Score Ditemukan: {self.best_eval}")
        
        print("\n--- STATE AKHIR (HASIL) ---")
        print(self.best_state)
        print(f"Total Kontainer: {self.best_state.total_kontainer()}")
        print(f"Skor Akhir Terbaik: {self.best_eval}")
        print("------------------------------\n")

        print("Tutup window plot untuk melanjutkan program")
        self._plot_scores()

        return