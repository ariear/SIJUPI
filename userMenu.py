import os
import pandas as pd

def daftarBarang():
    os.system('cls')
    daftar_produk = pd.read_csv('db/products.csv')
    daftar_produk.index = daftar_produk.index + 1
    print(f"\n{'Daftar Pupuk dan Alat Pertanian':^40}\n")
    print(daftar_produk)

    return input("\nDaftar Menu:\n1. Beli Barang\n2. Tambah Wishlist Barang\n3. Kembali\nPilih berdasarkan nomor menu : ")
    # os.system('cls')