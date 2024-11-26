import os
import pandas as pd
import csv
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

def beli_barang():
    while True:
        # os.system('cls')
        barang = input("\nSilahkan Masukkan Nama Produk Yang Ingin Dibeli\n(jika barang lebih dari 1 maka bisa dipisah dengan ','): ")
        barang = barang.split(",")
        
        error = False
        barang_fix = []
        df = pd.read_csv('db/products.csv')
        for item in barang:
            data = df[df['Nama Produk'] == item.title().strip()]
            
            if not data.empty:
                stock = data['Stock'].values[0]
                if int(stock) > 0:
                    barang_fix.append(item.title().strip())
                else:
                    print(f"\nMaaf Stock dari {item} sudah habis...")
                    error = True
                    break
            else:
                print(f"\nKami tidak menjual {item}!")
                error = True
                break
        if error == False:
            break
    
    quantitas = []
    for item in barang:
        data = df[df['Nama Produk'] == item.title().strip()]
        stock = data['Stock'].values[0]
        
        while True :
            try :
                qty = int(input(f"\nBerapa banyak {item} yang akan dibeli?: "))
                if qty > 0:
                    if stock >= qty:
                        quantitas.append(qty)
                    else:
                        print(f"\nMaaf, Stock dari {item} tidak mencukupi...")
                        continue
                else:
                    print(f"\nInput harus lebih dari 0")
                    continue
                break
            except ValueError:
                print("\nInput Harus Berupa Angka!")
                continue
            
    while True:
        print("\nMetode Pembayaran:\n1. Cash\n2. Transfer")
        bayar = input("Silahkan Pilih Metode Pembayaran Sesuai Nomornya: ")
        if int(bayar) and int(bayar) == 1:
            bayar = "Cash"
            break
        elif int(bayar) and int(bayar) == 2:
            bayar = "Transfer"
            break
        else:
            print("\nHarap Masukkan Input Yang Valid!")
            continue
        
    return [barang, quantitas, bayar]



def read() :
    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1
    print(data)

def add():
    if not os.path.exists('db/products.csv'):
        with open('db/products.csv', mode='w', newline='') as file :
            csv_writer = csv.writer(file)
            header = ('Nama Produk', 'Jenis', 'Harga', 'Stock')
            csv_writer.writerow(header)

    Nama = input("Nama Produk\t: ")
    Jenis = input("Jenis\t: ")
    Harga = input("Harga\t: ")
    Stock = int(input("Stock\t: "))
    with open('db/products.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)

        csv_writer.writerow((Nama, Jenis, Harga, Stock))
    
    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1
    print("Data berhasil ditambahkan.")
    print(data)

def update():
    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1
    print(data)
        
    id_update = int(input("Masukkan ID yang ingin diupdate : ")) - 1
    
    Nama = input("Nama Produk\t: ")
    Jenis = input("Jenis\t: ")                
    Harga = int(input("Harga\t: "))
    Stock = int(input("Stock\t: "))
    
    data.iloc[id_update] = [Nama, Jenis, Harga, Stock]
    data.to_csv('db/products.csv', index=False)
    print("Data telah diupdate!")
    print(data)
    
def delete():
    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1
    print(data)

    id_del = int(input("Masukkan Id yang ingin dihapus: "))
    answer = ["iya", "tidak"]
    quest = input("Yakin ingin menghapus produk tersebut? (iya/tidak) : ")
    if quest in answer : 
        if quest == "iya" :
            if id_del in data.index :
                if id_del in data.index :
                    data = data.drop(id_del)
                    data.to_csv('db/products.csv', index=False)
                    print("Data berhasil dihapus!")
                    print(data)
            else :
                print("Masukkan index dengan benar!")
        else :
            print("Silahkan pilih menu lainnya")
    else :
        print("Masukkan jawaban dengan benar!")


def kelola() :
    os.system('cls')
    while True:
        print("Menu:")
        print("1. Tambah Data")
        print("2. Baca Data")
        print("3. Update Data")
        print("4. Hapus Data")
        print("5. Keluar")
        choice = input("Pilih opsi: ")
        os.system('cls')

        if choice == '1':
            add()
        elif choice == '2':
            read()
        elif choice == '3':
            update()
        elif choice == '4':
            delete()
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid.")