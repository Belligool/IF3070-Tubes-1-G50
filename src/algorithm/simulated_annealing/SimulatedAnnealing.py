import math
import random
import time
from bin.state import State
from bin.entity.kontainer import Kontainer
from bin.objective_function import objective_function as evaluate

class SimulatedAnnealing:
    def __init__(self, initial_state, kapasitas, temp_awal, alpha, n_iterations):
        self.kapasitas = kapasitas
        self.n_iterations = n_iterations
        self.temp_awal = temp_awal
        self.alpha = alpha

        self.current_state = initial_state
        self.current_eval = evaluate(self.current_state, self.kapasitas)
        self.best_state = self.current_state
        self.best_eval = self.current_eval

        self.scores_history = [self.best_eval]
        self.temp_history = [self.temp_awal]
        self.prob_history = []

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
                dest_k = random.choice([k for k in kontainers if k is not src_k])
            
            if not dest_k.tambah_barang(barang):
                src_k.tambah_barang(barang)
                if dest_k.total_isi() == 0 and dest_k not in state.kontainer_list:
                    new_state.kontainer_list.remove(dest_k)
        
        elif move_type == 'swap':
            k1, k2 = random.sample(non_empty_kontainers, 2)
            b1 = random.choice(k1.isi)
            b2 = random.choice(k2.isi)

            if (k1.total_isi() - b1.ukuran + b2.ukuran <= self.kapasitas) and (k2.total_isi() - b2.ukuran + b1.ukuran <= self.kapasitas):
                k1.hapus_barang(b1)
                k2.hapus_barang(b2)
                k1.tambah_barang(b2)
                k2.tambah_barang(b1)
        
        new_state.kontainer_list = [k for k in new_state.kontainer_list if k.total_isi() > 0]
        
        return new_state
    
    def run(self):
        print("--- Memulai Simulated Annealing ---")
        start_time = time.time()

        t = self.temp_awal

        for i in range(self.n_iterations):
            candidate = self.get_random_neighbour(self.current_state)
            candidate_eval = evaluate(candidate, self.kapasitas)
            delta_e = candidate_eval - self.current_eval

            if delta_e < 0:
                self.current_state, self.current_eval = candidate, candidate_eval
                
                if candidate_eval < self.best_eval:
                    self.best_state, self.best_eval = candidate, candidate_eval
            else:
                if t > 0.000001:
                    try:
                        prob = math.exp(-delta_e / t)

                        if random.random() < prob:
                            self.current_state, self.current_eval = candidate, candidate_eval
                            self.prob_history.append(prob)
                    except OverflowError:
                        prob = 0
            t *= self.alpha
            self.scores_history.append(self.best_eval)
            self.temp_history.append(t)

            if i % (self.n_iterations // 20) == 0:
                print(f"Iter: {i:>5} / {self.n_iterations}, Temp {t:8.3f}, Best {self.best_eval:8.2f}, Current {self.current_eval:8.2f}")
        
        end_time = time.time()
        print("--- Simulated Annealing Selesai!!! ---")
        print(f"Durasi: {end_time - start_time:.4f} detik.")
        print(f"Best score: {self.best_eval}")

        return self.best_state, self.best_eval, self.scores_history, self.temp_history, self.prob_history