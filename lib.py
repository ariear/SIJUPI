import os
import pandas as pd
from auth import enkripsi_password, verifikasi_password
from auth import role_parse

def info_akun(username):
    os.system('cls')
    accounts = pd.read_csv('db/accounts.csv')
    account = accounts[accounts['Username'] == username].iloc[0]
    
    while True:
        print(f"\n{'INFO AKUN':^30}\n")
        print(f"Username  : {account['Username']}")
        print(f"Role      : {role_parse(account['Role'])}")
        print("\n1. Update Username\n2. Update Password\n3. Kembali ke Menu Utama\n")
        pilih = input("Pilih berdasarkan nomor: ")
        
        match pilih:
            case '1':
                os.system('cls')
                print(f"{'UPDATE USERNAME':^30}\n")
                
                while True:
                    new_username = input(f"Masukkan Username baru : ").strip()
                    if new_username and len(new_username) >= 3:
                        if accounts[accounts['Username'] == new_username].empty or new_username == account['Username']:
                            accounts.loc[accounts['Username'] == username, 'Username'] = new_username
                            accounts.to_csv('db/accounts.csv', index=False)
                            username = new_username
                            print("\nUsername berhasil diperbarui!")
                            break
                        else:
                            print("Username sudah digunakan oleh akun lain!\n")
                    else:
                        print("Username minimal harus 3 karakter dan tidak boleh kosong!\n")
                
                input("\nTekan Enter untuk kembali...")
                os.system('cls')
                return username
            case '2':
                os.system('cls')
                print(f"{'UPDATE PASSWORD':^30}\n")
                
                while True:
                    old_password = input("Masukkan Password lama: ").strip()
                    if verifikasi_password(account['Password'], old_password):
                        break
                    else:
                        os.system('cls')
                        print(f"{'UPDATE PASSWORD':^30}\n")
                        print("Password lama salah!\n")
                
                while True:
                    new_password = input("Masukkan Password baru (minimal 8 karakter): ").strip()
                    if new_password and len(new_password) >= 8:
                        confirm_password = input("Konfirmasi Password baru: ").strip()
                        if new_password == confirm_password:
                            accounts.loc[accounts['Username'] == username, 'Password'] = enkripsi_password(new_password)
                            accounts.to_csv('db/accounts.csv', index=False)
                            print("\nPassword berhasil diperbarui!")
                            break
                        else:
                            print("Password baru dan konfirmasi tidak cocok!\n")
                    else:
                        print("Password minimal harus 8 karakter dan tidak boleh kosong!\n")
                
                input("\nTekan Enter untuk kembali...")
                os.system('cls')
                return username
            case '3':
                os.system('cls')
                return username
            case _:
                os.system('cls')
                print("\nInput harus ada di menu dan berupa angka!\n")
                continue

def daftarBarang():
    daftar_produk = pd.read_csv('db/products.csv')
    daftar_produk.index = daftar_produk.index + 1
    print(f"\n{'Daftar Pupuk dan Alat Pertanian':^40}\n")
    print(daftar_produk)

    return input("\nDaftar Menu:\n1. Beli Produk\n2. Tambah Wishlist Produk\n3. Kembali\nPilih berdasarkan nomor menu : ")


def tambah_wishlist(username):
    os.system('cls')
    daftar_produk = pd.read_csv('db/products.csv')
    daftar_produk.index = daftar_produk.index + 1

    wishlist = pd.read_csv('db/wishlists.csv')

    while True:
        print(f"\n{'TAMBAH WISHLIST PRODUK':^40}\n")
        print(daftar_produk)
        
        try:
            pilihan = int(input("\nPilih produk berdasarkan nomor (0 untuk keluar): "))
            if pilihan == 0:
                os.system('cls')
                break
            elif 1 <= pilihan <= len(daftar_produk):
                barang = daftar_produk.iloc[pilihan - 1]
                nama_produk = barang['Nama Produk']
                harga = barang['Harga']

                if not wishlist[(wishlist['Username'] == username) & (wishlist['Nama Produk'] == nama_produk)].empty:
                    os.system('cls')
                    print(f"\n{nama_produk} sudah ada di wishlist Anda!")
                else:
                    new_entry = pd.DataFrame({'Username': [username], 'Nama Produk': [nama_produk], 'Harga': [harga]})
                    wishlist = pd.concat([wishlist, new_entry], ignore_index=True)
                    wishlist.to_csv('db/wishlists.csv', index=False)
                    
                    os.system('cls')
                    print(f"\n{nama_produk} berhasil ditambahkan ke wishlist!")
            else:
                os.system('cls')
                print("\nPilihan tidak ada, coba lagi.")
        except ValueError:
            os.system('cls')
            print("\nInput harus berupa angka, coba lagi.")


def lihat_wishlist(username):
    os.system('cls')

    wishlists = pd.read_csv('db/wishlists.csv')
    user_wishlists = wishlists[wishlists['Username'] == username]

    os.system('cls')
    print(f"\n{'WISHLIST ANDA':^40}\n")
    if user_wishlists.empty:
        print("Kamu belum memiliki produk di wishlist.")
    else:
        user_wishlists = user_wishlists.reset_index(drop=True)
        user_wishlists.index += 1

        print(user_wishlists[['Nama Produk', 'Harga']])
    
    input("\nTekan Enter untuk kembali...")
    os.system('cls')
