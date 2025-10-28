from initializer import generate_initial_state
from algorithm.hill_climbing.steepest_ascent.SteepestAscent import SteepestAscent
from algorithm.genetic.Genetic import GeneticAlgorithm
from algorithm.simulated_annealing.SimulatedAnnealing import SimulatedAnnealing
from utils import load_input

def main_menu():
    print("==================================START===================================")
    print(r"""
    ___________________________________________________________________
                        
    IRASSHAIMASE! Selamat Datang di Bin Packing Optimizer!

    ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
    ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
    ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
    ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
    ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
    ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝      
                                                     
    ___________________________________________________________________
    """)

    while True:
        print("=====================================================================")
        print("""
            +-------------------------------+
            |     PILIH ALGORITMA YANG      |
            |          INGIN DICOBA         |
            +-------------------------------+
        """)
        print("1. Steepest Ascent Hill-Climbing")
        print("2. Simulated Annealing")
        print("3. Genetic Algorithm")
        print("4. Keluar dari program")

        pilihan = input("Masukkan nomor opsi (1-4): ")

        if pilihan == '1':
            print("\nAnda memilih Steepest Ascent Hill-Climbing.")

            filename = input("Masukkan nama file input (misal: input.json): ")
            kapasitas, barang_list = load_input(filename)

            # ===============================
            # Buat state awal
            # ===============================
            initial_state = generate_initial_state(barang_list, kapasitas)

            # ===============================
            # Jalankan algoritma
            # ===============================
            algo = SteepestAscent(initial_state, kapasitas)
            algo.run()  
        
        elif pilihan == '2':
            print("\nAnda memilih Simulated Annealing.")
            filename = input("Masukkan nama file input (misal: input.json): ")
            try:
                kapasitas, barang_list = load_input(filename)
            except FileNotFoundError:
                print(f"Error: File '{filename}' tidak ditemukan.")
                continue

            initial_state = generate_initial_state(barang_list, kapasitas)
            print("\n--- 🏁 STATE AWAL ---")
            print(initial_state)
            print(f"Skor Awal: {objective_function(initial_state, kapasitas)}")
            print("-----------------------\n")

            try:
                temp_awal = float(input("Masukkan Temperatur Awal (misal: 1000): "))
                alpha = float(input("Masukkan Cooling Rate/Alpha (misal: 0.99): "))
                n_iterations = int(input("Masukkan Jumlah Iterasi (misal: 10000): "))
            except ValueError:
                print("Error: Input tidak valid. Harap masukkan angka.")
                continue
        
            algo = SimulatedAnnealing(initial_state, kapasitas, temp_awal, alpha, n_iterations)
            best_state, best_score, scores_history, temp_history, prob_history = algo.run()

            print("\n--- 🏆 STATE AKHIR (HASIL) ---")
            print(best_state)
            print(f"Total Kontainer: {best_state.total_kontainer()}")
            print(f"Skor Akhir Terbaik: {best_score}")
            print("------------------------------\n")


        elif pilihan == '2':
            print("\nAnda memilih Simulated Annealing.")
            print("Fitur ini masih dalam pengembangan. Silakan coba algoritma lain.")

        elif pilihan == '3':
            print("\nAnda memilih Genetic Algorithm.")

            filename = input("Masukkan nama file input (misal: input.json): ")
            kapasitas, barang_list = load_input(filename)

            # ===============================
            # Buat state awal
            # ===============================
            initial_state = generate_initial_state(barang_list, kapasitas)

            # ===============================
            # Jalankan algoritma
            # ===============================
            ga = GeneticAlgorithm(initial_state, kapasitas)
            ga.run()

        elif pilihan == '4':
            print("Terima kasih telah menggunakan program ini. Keluar...")
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

# Panggilan fungsi main
if __name__ == "__main__":
    main_menu()
    print(r"""
    _______________________________________________________________________________
                        
    SAYONARA! Terima kasih telah menggunakan Bin Packing Optimizer!
          
    ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗
    ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║
       ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║
       ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║
       ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ 
                                                                                                 
    ________________________________________________________________________________
    """)

    print("===========================END===========================")