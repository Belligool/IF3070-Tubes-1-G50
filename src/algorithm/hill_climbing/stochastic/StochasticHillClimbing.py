# src/algorithm/hill_climbing/stochastic/StochasticHillClimbing.py

import math
import random
import time
import matplotlib.pyplot as plt
from bin.state import State
from bin.entity.kontainer import Kontainer
from bin.objective_function import objective_function as evaluate

class StochasticHillClimbing:

    def __init__(self, initial_state, kapasitas):
        self.kapasitas = kapasitas

        self.current_state = initial_state
        self.current_eval = evaluate(self.current_state, self.kapasitas)
        self.best_state = self.current_state
        self.best_eval = self.current_eval
        
        # Riwayat untuk plot
        self.scores_history = [self.best_eval]
        self.current_scores_history = [self.current_eval]

    def get_random_neighbour(self, state):
        new_state = state.clone()
        kontainers = new_state.kontainer_list

        non_empty_kontainers = [k for k in kontainers if k.total_isi() > 0]
        if not non_empty_kontainers:
            return new_state 

        move_type = 'move'
        if len(non_empty_kontainers) >= 2:
            move_type = random.choice(['move', 'swap'])

        if move_type == 'move':
            src_k = random.choice(non_empty_kontainers)
            barang = random.choice(src_k.isi)
            src_k.hapus_barang(barang)

            if random.random() < 0.1 or len(kontainers) == 1:
                dest_k = Kontainer(self.kapasitas)
                new_state.kontainer_list.append(dest_k)
            else:
                possible_dests = [k for k in kontainers if k is not src_k]
                if not possible_dests:
                     dest_k = src_k
                else:
                     dest_k = random.choice(possible_dests)

            if not dest_k.tambah_barang(barang):
                src_k.tambah_barang(barang)
                if dest_k.total_isi() == 0 and dest_k not in state.kontainer_list:
                    new_state.kontainer_list.remove(dest_k)

        elif move_type == 'swap':
            k1, k2 = random.sample(non_empty_kontainers, 2)
            b1 = random.choice(k1.isi)
            b2 = random.choice(k2.isi)
            
            if (k1.total_isi() - b1.ukuran + b2.ukuran <= self.kapasitas) and \
               (k2.total_isi() - b2.ukuran + b1.ukuran <= self.kapasitas):
                
                k1.hapus_barang(b1)
                k2.hapus_barang(b2)
                k1.tambah_barang(b2)
                k2.tambah_barang(b1)
        
        new_state.kontainer_list = [k for k in new_state.kontainer_list if k.total_isi() > 0]
        
        return new_state

    def _plot_scores(self):
        plt.figure(figsize=(12, 7))
        
        plt.plot(self.scores_history, 
                 label="Best Score", 
                 color="blue", 
                 linewidth=2)
        
        plt.plot(self.current_scores_history, 
                 label="Current Score", 
                 color="orange",
                 alpha=0.5,
                 linestyle='--',
                 linewidth=1)
        
        plt.title("Best Score vs Current Score (Stochastic HC)")
        plt.xlabel("Iteration")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True)
        print("Menampilkan Plot Skor (Best vs Current)...")
        plt.show()

    def run(self):
        print("\n--- STATE AWAL ---")
        print(self.current_state)
        print(f"Skor Awal: {self.current_eval}")
        print("-----------------------\n")
        
        max_stall_iterations = int(input("Masukkan Max Stall Iterations (batas gagal berturut-turut, misal: 1000): "))
            
        print("--- Memulai Stochastic Hill Climbing ---")
        start_time = time.time()
        
        iteration = 0
        stall_counter = 0
        
        while True:
            neighbor = self.get_random_neighbour(self.current_state)
            neighbor_eval = evaluate(neighbor, self.kapasitas)
            
            if neighbor_eval < self.current_eval:
                self.current_state = neighbor
                self.current_eval = neighbor_eval
                stall_counter = 0
                
                if self.current_eval < self.best_eval:
                    self.best_eval = self.current_eval
                    self.best_state = self.current_state
            
            else:
                stall_counter += 1

            self.scores_history.append(self.best_eval)
            self.current_scores_history.append(self.current_eval)
            
            if stall_counter >= max_stall_iterations:
                print(f"\nBatas maksimum stall ({max_stall_iterations}) tercapai. Berhenti.")
                break
            
            if iteration % 100 == 0:
                print(f"Iter: {iteration}, Best: {self.best_eval:.2f}, Current: {self.current_eval:.2f}, Stalls: {stall_counter}/{max_stall_iterations}", end='\r')
            
            iteration += 1

        print()
        end_time = time.time()
        duration = end_time - start_time
        
        print("--- Stochastic Hill Climbing Selesai ---")
        print(f"Durasi: {duration:.4f} detik")
        print(f"Berhenti setelah {iteration} total iterasi")
        print(f"Best Score Ditemukan: {self.best_eval}")

        print("\n--- STATE AKHIR (HASIL) ---")
        print(self.best_state)
        print(f"Total Kontainer: {self.best_state.total_kontainer()}")
        print(f"Skor Akhir Terbaik: {self.best_eval}")
        print("------------------------------\n")

        print("Tutup window plot untuk melanjutkan program")
        self._plot_scores()

        return