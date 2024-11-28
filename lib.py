import os
import pandas as pd
import csv
import random
from auth import enkripsi_password, verifikasi_password, daftar_huruf
from auth import role_parse
from datetime import datetime

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

    header = "| {:^5} | {:^29} | {:^10} | {:^15} | {:^5} |".format("No", "Nama Produk", "Jenis", "Harga", "Stok")
    garis = "-"* 79


    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'Daftar Pupuk dan Alat Pertanian':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    print(garis)
    print(header)
    print(garis)

    for id, row in daftar_produk.iterrows():
        print("| {:^5} | {:<29} | {:>10} | {:>15} | {:>5} |".format(id, row['Nama Produk'], row['Jenis'], row['Harga'], row['Stock']))
        print(garis)


def tambah_wishlist(username):
    os.system('cls')
    daftar_produk = pd.read_csv('db/products.csv')
    daftar_produk.index = daftar_produk.index + 1

    wishlist = pd.read_csv('db/wishlists.csv')

    while True:
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'TAMBAH WISHLIST PRODUK':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)
        daftarBarang()
        
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
                    print(f"\n{nama_produk + ' sudah ada di wishlist Anda!':^78}")
                else:
                    new_entry = pd.DataFrame({'Username': [username], 'Nama Produk': [nama_produk], 'Harga': [harga]})
                    wishlist = pd.concat([wishlist, new_entry], ignore_index=True)
                    wishlist.to_csv('db/wishlists.csv', index=False)
                    
                    os.system('cls')
                    print(f"\n{nama_produk + 'berhasil ditambahkan ke wishlist!':^78}")
            else:
                os.system('cls')
                print(f"\n{'Pilihan tidak ada, coba lagi.':^78}")
        except ValueError:
            os.system('cls')
            print(f"\n{'Input harus berupa angka, coba lagi.':^78}")


def lihat_wishlist(username):
    os.system('cls')

    wishlists = pd.read_csv('db/wishlists.csv')
    user_wishlists = wishlists[wishlists['Username'] == username]

    os.system('cls')
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'WISHLIST ANDA':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    if user_wishlists.empty:
        print("Kamu belum memiliki produk di wishlist.")
    else:
        user_wishlists = user_wishlists.reset_index(drop=True)
        user_wishlists.index += 1

        header = "| {:^5} | {:^28} | {:^37} |".format("No", "Nama Produk", "Harga")
        garis = "-"* 79
        print(garis)
        print(header)
        print(garis)
        for id, row in user_wishlists.iterrows():
            print("| {:^5} | {:<28} | {:>37} |".format(id, row['Nama Produk'], row['Harga']))
            print(garis)
    
    input("\nTekan Enter untuk kembali...")
    os.system('cls')

def beli_barang(username):
    os.system('cls')
    while True:
        df = pd.read_csv('db/products.csv')
        daftarBarang()
        
        barang_fix = []
        quantitas = []
        daftar_harga = []
        
        while True:
            try:
                pilihan = int(input("\nMasukkan nomor produk yang ingin dibeli: "))
                if 1 <= pilihan <= len(df):
                    item = df.iloc[pilihan-1]
                    nama_produk = item['Nama Produk']
                    harga = item['Harga'] 
                    stock = item['Stock']
                    
                    while True:
                        try:
                            qty = int(input(f"Berapa banyak {nama_produk} yang ingin dibeli?: "))
                            if qty > 0:
                                if qty <= stock:
                                    barang_fix.append(nama_produk)
                                    quantitas.append(qty)
                                    daftar_harga.append(harga)

                                    df.loc[pilihan-1, 'Stock'] = stock - qty

                                    print(f"\n{str(qty) + ' ' + nama_produk + ' berhasil ditambahkan ke daftar pembelian.':^78}")
                                    break
                                else:
                                    print(f"\nMaaf, stok {nama_produk} hanya tersedia {stock}.")
                            else:
                                print("\nJumlah harus lebih dari 0.")
                        except ValueError:
                            print("\nInput harus berupa angka!")
                else:
                    print("\nNomor produk tidak ada!!")
            except ValueError:
                print("\nInput harus berupa angka!")
            
            while True:
                print("\nIngin membeli barang lagi?\n1. Ya\n2. Tidak")
                lagi = input("Pilih (1/2): ")
                if lagi == "1":
                    break
                elif lagi == "2":
                    break
                else:
                    print("\nInput tidak valid, coba lagi.")
            if lagi == "1":
                os.system('cls')
                daftarBarang()
                continue
            elif lagi == "2":
                os.system('cls')
                daftarBarang()
                break
        
        while True:
            print("\nMetode Pembayaran:\n1. Cash\n2. Transfer")
            bayar = input("Silahkan Pilih Metode Pembayaran Sesuai Nomornya: ")
            if bayar == "1":
                bayar = "Cash"
                break
            elif bayar == "2":
                bayar = "Transfer"
                break
            else:
                print(f"\n{'Harap Masukkan Input Yang Valid!':^78}")


        transaksi_df = pd.read_csv('db/transactions.csv')

        transaksi_id = ''.join(random.choices(daftar_huruf, k=6))
        tanggal_sekarang = datetime.now().strftime('%d-%m-%Y')
        transaksi_baru = []
        total_harga = 0
        for nama, harga, qty in zip(barang_fix, daftar_harga, quantitas):
            transaksi_baru.append({
                "Transaksi id": transaksi_id,
                "Username": username,
                "Nama Produk": nama,
                "Harga": harga,
                "Quantitas": qty,
                "Tipe Pembayaran": bayar,
                "Tanggal Pembuatan": tanggal_sekarang,
                "Tanggal Konfirmasi": "",
                "Konfirmasi": "",
                "Lunas": ""
            })
            total_harga += harga * qty
        
        transaksi_df = pd.concat([transaksi_df, pd.DataFrame(transaksi_baru)], ignore_index=True)
        transaksi_df.to_csv('db/transactions.csv', index=False)

        df.to_csv('db/products.csv', index=False)
        
        os.system('cls')
        print("=" * 78)
        print(f"\n{'Struk Pembayaran':^78}\n")
        print("=" * 78)
        print(f"Transaksi ID : {transaksi_id}")
        print(f"Username     : {username}")
        print(f"Tanggal      : {tanggal_sekarang}")
        print(f"Metode Bayar : {bayar}")
        print("-" * 78)
        print(f"{'Produk':<30} {'Harga':<15} {'Quantitas':<10} {'Subtotal':<15}")
        print("-" * 78)
        for nama, harga, qty in zip(barang_fix, daftar_harga, quantitas):
            subtotal = harga * qty
            print(f"{nama:<30} {harga:<15} {qty:<10} {subtotal:<15}")
        print("-" * 78)
        print(f"{'Total Harga':>65}: {total_harga}")
        print("=" * 78)

        if bayar == "Transfer":
            print("\nSilahkan transfer ke rekening berikut untuk menyelesaikan transaksi:")
            print("Bank ABC, No. Rekening: 1234567890, a.n. Toko SIJUPI\n")
            print("=" * 78)
        
        return input('Tekan enter untuk keluar.....')


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