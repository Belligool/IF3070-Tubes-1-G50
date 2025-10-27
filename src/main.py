import time
import random
from initializer import generate_initial_state
from bin.objective_function import objective_function
from bin.neighbor_state import generate_neighbors
from bin.entity.barang import Barang
from algorithm.hill_climbing.steepest_ascent.SteepestAscent import SteepestAscent
from utils import load_input

def main_menu():
    print("==================================START===================================")
    print(r"""
    ________________________________________________
                        
    IRASSHAIMASE! Selamat Datang di Bin Packing Optimizer!

    ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
    ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
    ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
    ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
    ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
    ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝      
                                                     
    ________________________________________________
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

            # ===============================
            # Inisialisasi data barang dari file input
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

        elif pilihan == '4':
            print("Terima kasih telah menggunakan program ini. Keluar...")
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

# Panggilan fungsi main
if __name__ == "__main__":
    main_menu()
    print(r"""
    ________________________________________________
                        
    SAYONARA! Terima kasih telah menggunakan Bin Packing Optimizer!
          
    ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗
    ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║
       ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║
       ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║
       ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ 
                                                                                                 
    ________________________________________________
    """)
    print("===========================END===========================")