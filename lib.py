import os
import pandas as pd
import csv
import random
from auth import enkripsi_password, verifikasi_password, daftar_huruf, register
from auth import role_parse
from datetime import datetime

def daftar_transaksi(username):
    os.system('cls')
    while True:
        transaksi_df = pd.read_csv('db/transactions.csv')
        
        user_transaksi = transaksi_df[transaksi_df['Username'] == username]
        
        if user_transaksi.empty:
            print("=" * 78)
            print(f"{'Kamu belum pernah melakukan transaksi.':^78}")
            print("=" * 78)
            input("\nTekan enter untuk kembali...")
            return
        
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'Daftar Pembelian':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)
        
        print(f"| {'No':<5} {'Transaksi ID':<15} {'Tanggal':<15} {'Total Harga':<18} {'Status':<20}|")
        print("-" * 80)
        
        grouped_transaksi = user_transaksi.groupby("Transaksi id")
        daftar_transaksi = []
        for i, (transaksi_id, group) in enumerate(grouped_transaksi, start=1):
            total_harga = (group['Harga'] * group['Quantitas']).sum()
            status = "Lunas" if group['Lunas'].iloc[0] == True else "Belum Lunas"
            daftar_transaksi.append(transaksi_id)
            tanggal = group['Tanggal Pembuatan'].iloc[0]

            print(f"| {i:<5} {transaksi_id:<15} {tanggal:<15} {total_harga:<18} {status:<20}|")
        
        print("-" * 80)
        
        print("\n1. Lihat Struk")
        print("2. Kembali")
        
        pilihan = input("\nPilih menu (1/2): ")
        if pilihan == "1":
            try:
                transaksi_pilihan = int(input("Pilih transaksi berdasarkan nomor : "))
                if 1 <= transaksi_pilihan <= len(daftar_transaksi):
                    transaksi_id = daftar_transaksi[transaksi_pilihan - 1]
                    transaksi_detail = user_transaksi[user_transaksi['Transaksi id'] == transaksi_id]
                    
                    os.system('cls')
                    print("=" * 78)
                    print(f"\n{'Struk Pembayaran':^78}\n")
                    print("=" * 78)
                    print(f"Transaksi ID : {transaksi_id}")
                    print(f"Username     : {username}")
                    print(f"Tanggal      : {transaksi_detail['Tanggal Pembuatan'].iloc[0]}")
                    print(f"Metode Bayar : {transaksi_detail['Tipe Pembayaran'].iloc[0]}")
                    print("-" * 78)
                    print(f"{'Produk':<30} {'Harga':<15} {'Quantitas':<10} {'Subtotal':<15}")
                    print("-" * 78)
                    total_harga = 0
                    for _, row in transaksi_detail.iterrows():
                        subtotal = row['Harga'] * row['Quantitas']
                        total_harga += subtotal
                        print(f"{row['Nama Produk']:<30} {row['Harga']:<15} {row['Quantitas']:<10} {subtotal:<15}")
                    print("-" * 78)
                    print(f"{'Total Harga':>65}: {total_harga}")
                    print("=" * 78)
                    print("\n")
                    input("Tekan enter untuk keluar....")
                    os.system('cls')
                else:
                    os.system('cls')
                    print(f"\n{'Transaksi tidak ada!! Pilih berdasarkan nomor!!':^78}")
            except ValueError:
                os.system('cls')
                print(f"\n{'Input harus berupa angka!':^78}")
        elif pilihan == "2":
            os.system('cls')
            return
        else:
            os.system('cls')
            print(f"\n{'Input harus ada di menu dan berupa angka!':^78}")


def info_akun(username):
    os.system('cls')
    accounts = pd.read_csv('db/accounts.csv')
    account = accounts[accounts['Username'] == username].iloc[0]
    
    while True:
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'INFO AKUN':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)
        
        print(f"|    {'Username  : ' + account['Username']:<74}|")
        print(f"|    {'Role      : ' + role_parse(account['Role']):<74}|")
        print("-"*80)

        print(f"|{'     Daftar menu :':<78}|")
        print(f"|{'     1. Update Username':<78}|")
        print(f"|{'     2. Update Password':<78}|")
        print(f"|{'     3. Kembali':<78}|")
        print(f"|{' ' * 78}|")
        print("-" * 80)
        pilih = input("Pilih berdasarkan nomor: ")
        
        match pilih:
            case '1':
                os.system('cls')
                print("-"*80)
                print(f"|{' ' * 78}|")
                print(f"|{'UPDATE USERNAME':^78}|")
                print(f"|{' ' * 78}|")
                print("-"*80)
                
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
                print("-"*80)
                print(f"|{' ' * 78}|")
                print(f"|{'UPDATE PASSWORD':^78}|")
                print(f"|{' ' * 78}|")
                print("-"*80)
                
                while True:
                    old_password = input("Masukkan Password lama: ").strip()
                    if verifikasi_password(account['Password'], old_password):
                        break
                    else:
                        os.system('cls')
                        print("-"*80)
                        print(f"|{' ' * 78}|")
                        print(f"|{'UPDATE PASSWORD':^78}|")
                        print(f"|{' ' * 78}|")
                        print("-"*80)
                        print(f"\n{'⚠  Password lama salah! ⚠':^78}\n")
                
                while True:
                    new_password = input("Masukkan Password baru (minimal 8 karakter): ").strip()
                    if new_password and len(new_password) >= 8:
                        confirm_password = input("Konfirmasi Password baru: ").strip()
                        if new_password == confirm_password:
                            accounts.loc[accounts['Username'] == username, 'Password'] = enkripsi_password(new_password)
                            accounts.to_csv('db/accounts.csv', index=False)
                            print(f"\n{'Password berhasil diperbarui!':^78}\n")
                            break
                        else:
                            print(f"\n{'⚠  Password baru dan konfirmasi tidak cocok! ⚠':^78}\n")
                    else:
                        print(f"\n{'⚠  Password minimal harus 8 karakter dan tidak boleh kosong! ⚠':^78}\n")
                
                input("\nTekan Enter untuk kembali...")
                os.system('cls')
                return username
            case '3':
                os.system('cls')
                return username
            case _:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
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

def update_wishlist(column = False, before = False, after = False):
    data_wishlist = pd.read_csv('db/wishlists.csv')
    data_wishlist.loc[data_wishlist[column] == before, column] = after

    data_wishlist.to_csv('db/wishlists.csv', index=False)


def lihat_wishlist(username):
    os.system('cls')
    while True:

        wishlists = pd.read_csv('db/wishlists.csv')
        user_wishlists = wishlists[wishlists['Username'] == username]

        print("-" * 80)
        print(f"|{' ' * 78}|")
        print(f"|{'WISHLIST ANDA':^78}|")
        print(f"|{' ' * 78}|")
        print("-" * 80)

        if user_wishlists.empty:
            print(f"\n{'Kamu belum memiliki produk di wishlist.':^78}\n")
        else:
            user_wishlists = user_wishlists.reset_index(drop=True)
            user_wishlists.index += 1

            header = "| {:^5} | {:^28} | {:^37} |".format("No", "Nama Produk", "Harga")
            garis = "-" * 79
            print(garis)
            print(header)
            print(garis)
            for id, row in user_wishlists.iterrows():
                print("| {:^5} | {:<28} | {:>37} |".format(id, row['Nama Produk'], row['Harga']))
                print(garis)

        print("\nMenu:")
        print("1. Hapus produk")
        print("2. Kembali")
        
        choice = input("Pilih menu (1/2): ").strip()

        if choice == '1':
            if user_wishlists.empty:
                input("\nWishlist kosong. Tekan Enter untuk kembali...")
                continue

            try:
                to_delete = int(input("\nPilih produk berdasarkan nomor : ").strip())
                if 1 <= to_delete <= len(user_wishlists):
                    selected_row = user_wishlists.iloc[to_delete - 1]
                    wishlists = wishlists[~((wishlists['Username'] == username) &
                                            (wishlists['Nama Produk'] == selected_row['Nama Produk']) &
                                            (wishlists['Harga'] == selected_row['Harga']))]
                    
                    wishlists.to_csv('db/wishlists.csv', index=False)
                    
                    print(f"\n{'Produk berhasil dihapus dari wishlist':^78}\n")
                else:
                    print(f"\n{'⚠  Produk yang kamu pilih tidak ada! Coba lagi ⚠':^78}\n")
            except ValueError:
                print(f"\n{'⚠  Masukkan nomor yang valid! ⚠':^78}\n")
            input("\nTekan Enter untuk kembali...")
            os.system('cls')
        
        elif choice == '2':
            os.system('cls')
            break
        else:
            os.system('cls')
            print(f"\n{'Input haru ada di menu dan berupa angka!':^78}\n")

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

            print("\nKonfirmasi pembayaran melalui nomor berikut : 0888382382382 \n")
            print("=" * 78)
        
        return input('Tekan enter untuk keluar.....')

def notificationMsg(penerima = False, pesan = False):
    if penerima and pesan:
        data_notif = pd.read_csv('db/notifications.csv')
        
        data_baru_list = []
        for topik in pesan:
            for akun in penerima:
                data_baru_list.append({
                    "Username": akun,
                    "Deskripsi": topik,
                    "Tanggal": datetime.now().strftime("%d-%m-%Y"),
                    "Terbaca": False
                })
        
        data_baru = pd.DataFrame(data_baru_list)
        
        data_notif = pd.concat([data_notif, data_baru], ignore_index=True)
        
        data_notif.to_csv("db/notifications.csv", index=False)
    return

def tambah_produk():
    if not os.path.exists('db/products.csv'):
        with open('db/products.csv', mode='w', newline='') as file :
            csv_writer = csv.writer(file)
            header = ('Nama Produk', 'Jenis', 'Harga', 'Stock')
            csv_writer.writerow(header)

    print("-" * 80)
    print(f"|{' ' * 78}|")
    print(f"|{'TAMBAH PRODUK':^78}|")
    print(f"|{' ' * 78}|")
    print("-" * 80)

    Nama, Jenis, Harga, Stock = None, None, None, None
    while True:
        if not Nama:
            Nama = input("Nama Produk\t: ").strip()
            if not Nama:
                print(f"\n{'⚠  Nama produk tidak boleh kosong ⚠':^78}\n")
                continue
        
        if not Jenis:
            Jenis = input("Jenis\t\t: ").strip()
            if not Jenis:
                print(f"\n{'⚠  Jenis produk tidak boleh kosong ⚠':^78}\n")
                continue

        if Harga is None:
            Harga_input = input("Harga\t\t: ").strip()
            try:
                Harga = int(Harga_input)
                if Harga < 0:
                    print(f"\n{'⚠  Harga harus berupa angka positif ⚠':^78}\n")
                    Harga = None
                    continue
            except ValueError:
                print(f"\n{'⚠  Harga harus berupa angka ⚠':^78}\n")
                continue

        if Stock is None:
            Stock_input = input("Stock\t\t: ").strip()
            if Stock_input.isdigit() and int(Stock_input) >= 0:
                Stock = int(Stock_input)
            else:
                print(f"\n{'⚠  Stock harus berupa angka positif ⚠':^78}\n")
                continue

        if Nama and Jenis and Harga is not None and Stock is not None:
            break
    
    with open('db/products.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)

        csv_writer.writerow((Nama, Jenis, Harga, Stock))
    
    os.system('cls')
    print(f"\n{'Produk berhasil ditambahkan!!':^78}\n")

def update_produk(errorMsg=False):
    os.system('cls')

    if errorMsg:
        print(f"\n{errorMsg:^78}\n")

    daftarBarang()

    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1

    try:
        id_update = int(input("\nPilih produk untuk diperbarui berdasarkan nomor : "))
    except ValueError:
        update_produk("Input harus berupa angka!")
        return

    if id_update in data.index:
        os.system('cls')
        while True:
            print(f"\n{'Produk terpilih: ' + data.loc[id_update, 'Nama Produk']:^78}")
            print("\nPilih data yang ingin diperbarui :")
            print("1. Ubah Nama Produk")
            print("2. Ubah Jenis")
            print("3. Ubah Harga")
            print("4. Ubah Stock")
            print("5. Batal")
            try:
                choice = int(input("\nPilih berdasarkan nomor : "))
            except ValueError:
                os.system('cls')
                print(f"\n{'Input harus berupa angka! Coba lagi':^78}\n")
                continue

            if choice == 1:
                Nama = input("Nama Produk Baru: ")
                if not Nama.strip():
                    os.system('cls')
                    print(f"\n{'Nama produk tidak boleh kosong! Coba lagi':^78}\n")
                    continue
                data.loc[id_update, "Nama Produk"] = Nama

                os.system('cls')
                print(f"\n{'Nama produk berhasil diperbarui menjadi ' + Nama:^78}\n")
            elif choice == 2:
                Jenis = input("Jenis Baru: ")
                if not Jenis.strip():
                    os.system('cls')
                    print(f"\n{'Jenis produk tidak boleh kosong! Coba lagi':^78}\n")
                    continue
                data.loc[id_update, "Jenis"] = Jenis

                os.system('cls')
                print(f"\n{'Jenis produk berhasil diperbarui menjadi ' + Jenis:^78}\n")
            elif choice == 3:
                try:
                    Harga = input("Harga Baru: ")
                    if not Harga.strip():
                        raise ValueError("Harga tidak boleh kosong!")
                    Harga = int(Harga)
                    data.loc[id_update, "Harga"] = Harga

                    os.system('cls')
                    print(f"\n{'Harga produk berhasil diperbarui menjadi ' + str(Harga):^78}\n")
                except ValueError:
                    os.system('cls')
                    print(f"\n{'Harga harus berupa angka! Coba lagi':^78}\n")
                    continue
            elif choice == 4:
                try:
                    Stock = input("Stock Baru: ")
                    if not Stock.strip(): 
                        raise ValueError("Stock tidak boleh kosong!")
                    Stock = int(Stock)
                    data.loc[id_update, "Stock"] = Stock

                    os.system('cls')
                    print(f"\n{'Stock produk berhasil diperbarui menajdi ' + str(Stock):^78}\n")
                except ValueError:
                    os.system('cls')
                    print(f"\n{'Stock harus berupa angka! Coba lagi':^78}\n")
                    continue
            elif choice == 5:
                os.system('cls')
                return
            else:
                os.system('cls')
                print(f"\n{'Pilih berdasarkan nomor menu!!':^78}\n")
                continue

            data.to_csv('db/products.csv', index=False)
            return
    else:
        update_produk(f"Produk yang kamu pilih tidak ada!")
        return

    
def hapus_produk():
    while True:
        daftarBarang()

        data = pd.read_csv('db/products.csv')
        data.index = data.index + 1

        try:
            id_del = int(input("\nPilih produk yang ingin dihapus berdasarkan No : "))
        except ValueError:
            os.system('cls')
            print(f"\n{'Input harus berupa angka! Coba lagi.':^78}\n")
            continue

        answer = ["iya", "tidak"]
        quest = input("Yakin ingin menghapus produk tersebut? (iya/tidak) : ")

        if quest in answer : 
            if quest == "iya" :
                if id_del in data.index :
                    if id_del in data.index :
                        data = data.drop(id_del)
                        data.to_csv('db/products.csv', index=False)
                        
                        os.system('cls')
                        print(f"\n{'Produk berhasil dihapus':^78}\n")
                        break
                else :
                    os.system('cls')
                    print(f"\n{'Produk tidak ada':^78}\n")
            else :
                os.system('cls')
                print(f"\n{'Silahkan pilih menu lainnya':^78}\n")
                break
        else :
            os.system('cls')
            print(f"\n{'Silahkan pilih menu lainnya':^78}\n")
            break


def kelola_produk() :
    os.system('cls')
    while True:
        daftarBarang()

        print("\nMenu:")
        print("1. Tambah Produk")
        print("2. Update Produk")
        print("3. Hapus Produk")
        print("4. Keluar")
        choice = input("Pilih menu: ")
        os.system('cls')

        if choice == '1':
            tambah_produk()
        elif choice == '2':
            update_produk()
        elif choice == '3':
            hapus_produk()
        elif choice == '4':
            break
        else:
            print(f"\n{'⚠  Masukkan nomor yang valid! ⚠':^78}\n")
        
def notif_sudah_terbaca(username = False):
    os.system('cls')
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'NOTIFIKASI SUDAH TERBACA':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    notif = pd.read_csv("db/notifications.csv")
    notif = notif[(notif["Username"] == username) & (notif["Terbaca"] == True)]
    notif = notif[["Deskripsi", "Tanggal"]]
    notifikasi = notif.values.tolist()

    print("\n{:^20}  {:} \n".format("Tanggal", "Deskripsi"))
    for item in notifikasi:
        print(f"{item[1]:^20}{item[0]}\n")
    input("Tekan Enter Untuk Kembali...")
    return

def notif_belum_terbaca(username=False):
    os.system('cls')
    print("-" * 80)
    print(f"|{' ' * 78}|")
    print(f"|{'NOTIFIKASI BELUM TERBACA':^78}|")
    print(f"|{' ' * 78}|")
    print("-" * 80)

    all_notif = pd.read_csv("db/notifications.csv")
    
    user_notif = all_notif[(all_notif["Username"] == username) & (all_notif["Terbaca"] == False)]
    
    if not user_notif.empty:
        tampilkan_notif = user_notif[["Deskripsi", "Tanggal"]]
        notifikasi = tampilkan_notif.values.tolist()

        print("\n{:^20}  {:} \n".format("Tanggal", "Deskripsi"))
        for item in notifikasi:
            print(f"{item[1]:^20}{item[0]}\n")
        
        all_notif.loc[(all_notif["Username"] == username) & (all_notif["Terbaca"] == False), "Terbaca"] = True
        
        all_notif.to_csv('db/notifications.csv', index=False)
    else:
        print(f"\n{'Tidak ada notifikasi untuk saat ini':^78}\n")

    input("Tekan Enter Untuk Kembali...")
    return

def notifikasi(username = False, errorMsg = False):
    data_notifikasi = pd.read_csv("db/notifications.csv")
    data_notifikasi = data_notifikasi[data_notifikasi["Username"] == username]
    count_unread = f"({len(data_notifikasi[data_notifikasi['Terbaca'] == False])})" if len(data_notifikasi[data_notifikasi['Terbaca'] == False]) > 0 else ""
        
    os.system('cls')
    
    if errorMsg:
        print(f"\n{errorMsg:^78}\n")
    
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'NOTIFIKASI':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    print(f"|{'     Daftar menu :':<78}|")
    print(f"|{'     1. Notifikasi Belum Terbaca ' + count_unread:<78}|")
    print(f"|{'     2. Notifikasi Sudah Terbaca ':<78}|")
    print(f"|{'     3. Kembali':<78}|")
    print(f"|{' ' * 78}|")
    print("-" * 80)
    
    menu = input("Silahkan Pilih Menu Notifikasi (1/2/3): ")
    
    if menu == "1":
        notif_belum_terbaca(username)
        notifikasi(username)
    elif menu == "2":
        notif_sudah_terbaca(username)
        notifikasi(username)
    elif menu == "3":
        os.system('cls')
        return
    else:
        notifikasi(username, "Input haru ada di menu dan berupa angka!")


def konfirmasi_pembelian():
    os.system('cls')
    while True:
        transaksi_df = pd.read_csv('db/transactions.csv')
        tf_belum_lunas = transaksi_df[transaksi_df['Lunas'] != True]

        if tf_belum_lunas.empty:
            print("=" * 78)
            print(f"{'Belum ada pembelian untuk dikonfirmasi':^78}")
            print("=" * 78)
            input("\nTekan enter untuk kembali...")
            return

        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'Daftar Pembelian yang belum dikonfirmasi':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)

        print(f"| {'No':<5} {'Transaksi ID':<15} {'Nama Pembeli':<20} {'Tanggal':<15} {'Total Harga':<17} |")
        print("-" * 80)

        grouped_transaksi = tf_belum_lunas.groupby("Transaksi id")
        daftar_transaksi = []
        for i, (transaksi_id, group) in enumerate(grouped_transaksi, start=1):
            total_harga = (group['Harga'] * group['Quantitas']).sum()
            daftar_transaksi.append(transaksi_id)
            tanggal = group['Tanggal Pembuatan'].iloc[0]

            print(f"| {i:<5} {transaksi_id:<15} {group['Username'].iloc[0]:<20} {tanggal:<15} {total_harga:<17} |")
        print("-" * 80)

        print("\nMenu:")
        print("1. Pilih berdasarkan nomor")
        print("2. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            try:
                nomor = int(input("Pilih transaksi berdasarkan nomor : "))
                if 1 <= nomor <= len(daftar_transaksi):
                    transaksi_id_pilih = daftar_transaksi[nomor - 1]
                    transaksi_df.loc[transaksi_df["Transaksi id"] == transaksi_id_pilih, ["Tanggal Konfirmasi", "Konfirmasi", "Lunas"]] = [datetime.now().strftime('%d-%m-%Y'), True, True]
                    transaksi_df.to_csv('db/transactions.csv', index=False)

                    os.system('cls')
                    print(f"\n{'Transaksi ID ' +  transaksi_id_pilih + ' berhasil dikonfirmasi!':^78}\n")
                else:
                    os.system('cls')
                    print(f"\n{'⚠  Transaksi tidak ada! Coba lagi ⚠':^78}\n")
            except ValueError:
                os.system('cls')
                print(f"\n{'⚠  Input harus berupa angka! ⚠':^78}\n")
        elif pilihan == "2":
            os.system('cls')
            break
        else:
            os.system('cls')
            print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
            

def hapus_akun(username = False, msg = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_dihapus = data_akun[data_akun["Username"] == username]
    data_akun = data_akun[data_akun["Username"] != username]
    
    if msg:
        print(msg)
    
    print("Akun Yang Akan Dihapus :\n")
    for id, row in data_dihapus.iterrows():
        role = role_parse(row['Role'])
        print("-"* 74)
        print("| {:^5} | {:^40} | {:^19} |".format(id, row['Username'], role))
        print("-"* 74)
    
    konfirmasi = input("\nApakah Anda Yakin ? (y/n): ")
    
    if konfirmasi == "y" or konfirmasi == "Y":
        data_akun.to_csv('db/accounts.csv', index=False)
        return True
    elif konfirmasi == "n" or konfirmasi == "N":
        return False
    else:
        return hapus_akun(username, "Input Tidak Valid!\n")

def update_username(username = False, msg = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_akun.index = data_akun.index + 1
    data_diubah = data_akun[data_akun["Username"] == username]
    
    if msg:
        print(msg)
    
    usernameBaru = input("\nSilahkan Masukkan Username Baru Untuk Akun Tersebut (Minimal 3 Character): ").strip()
    
    if not usernameBaru:
        return update_username(username, "Username tidak boleh hanya berupa spasi!")
    
    if len(usernameBaru) < 3:
        return update_username(username, "Username Akun Minimal 3 character!")

    data_akun.loc[data_akun["Username"] == username, "Username"] = usernameBaru
    
    print(f"\nUsername dari {username} akan diubah...\n{username}  ->  {usernameBaru}")
    
    konfirmasi = input("\nApakah Anda Yakin ? (y/n): ")
    
    if konfirmasi == "y" or konfirmasi == "Y":
        data_akun.to_csv('db/accounts.csv', index=False)
        return usernameBaru
    elif konfirmasi == "n" or konfirmasi == "N":
        return False
    else:
        return update_username(username, "Input Tidak Valid!\n")

def reset_password(username = False, msg = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_akun.index = data_akun.index + 1
    data_diubah = data_akun[data_akun["Username"] == username]
    
    if msg:
        print(msg)

    data_akun.loc[data_akun["Username"] == username, "Password"] = ""
    
    print(f"Password dari {username} akan direset...")
    
    konfirmasi = input("\nApakah Anda Yakin ? (y/n): ")
    
    if konfirmasi == "y" or konfirmasi == "Y":
        data_akun.to_csv('db/accounts.csv', index=False)
        return True
    elif konfirmasi == "n" or konfirmasi == "N":
        return False
    else:
        return reset_password(username, "Input Tidak Valid!\n")

def update_role(username = False, msg = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_akun.index = data_akun.index + 1
    data_diubah = data_akun[data_akun["Username"] == username]
    
    if msg:
        print(msg)
    
    print("\n🎟  ROLE:"
        +"\n1.  Admin"
        +"\n2.  Pembeli"
        +"\n")
    roleBaru = input("Silahkan Masukkan Role Baru Untuk Akun Tersebut (1/2): ")
    
    if not roleBaru.isdigit():
        return update_role(username, "Input Harus Berupa Nomor Dari List Role!")
    
    roleBaru = int(roleBaru)
    
    if roleBaru not in [1, 2]:
        return update_role(username, "Input Harus Berupa Nomor Dari List Role!")

    data_akun.loc[data_akun["Username"] == username, "Role"] = roleBaru
    
    role_awal = data_diubah["Role"].iloc[0]
    role_awal = role_parse(int(role_awal))
    role_baru = role_parse(roleBaru)
    
    print(f"\nRole dari {username} akan diubah...\n{role_awal}  ->  {role_baru}")
    
    konfirmasi = input("\nApakah Anda Yakin ? (y/n): ")
    
    if konfirmasi == "y" or konfirmasi == "Y":
        data_akun.to_csv('db/accounts.csv', index=False)
        return True
    elif konfirmasi == "n" or konfirmasi == "N":
        return False
    else:
        return update_role(username, "Input Tidak Valid!\n")

def menu_update(username = False, msg = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_dihapus = data_akun[data_akun["Username"] == username]
    
    if msg:
        print(msg)
    
    print("Akun Yang Akan Diperbarui :\n")
    for id, row in data_dihapus.iterrows():
        role = role_parse(row['Role'])
        print("-"* 74)
        print("| {:^5} | {:^40} | {:^19} |".format(id, row['Username'], role))
        print("-"* 74)
    
    print("\nMenu Perbarui:\n1. Perbarui Username\n2. Reset Password\n3. Perbarui Role\n4. Kembali")
    
    konfirmasi = input("\nSilahkan pilih menu dari list di atas (1/2/3/4): ")
    
    if konfirmasi == "1":
        result = update_username(username)
        if result:
            return menu_update(result, "Role Berhasil Diperbarui")
        else:
            return menu_update(username, "Role Batal Diperbarui")
    elif konfirmasi == "2":
        result = reset_password(username)
        if result:
            return menu_update(username, "Password Telah Direset!")
        else:
            return menu_update(username, "Password Batal Direset!")
    elif konfirmasi == "3":
        result = update_role(username)
        if result:
            return menu_update(username, "Role Berhasil Diperbarui")
        else:
            return menu_update(username, "Role Batal Diperbarui")
    elif konfirmasi == "4":
        return
    else:
        return menu_update(username, "Input Harus Berupa Angka Dan Sesuai Dengan Nomor Urut Menu!\n")
    

def daftar_akun(menu = False, msg = False, username = False):
    os.system('cls')
    data_akun = pd.read_csv('db/accounts.csv')
    data_akun = data_akun[["Username", "Role"]]
    data_akun = data_akun[data_akun["Username"] != username]
    data_akun.index = range(1, len(data_akun) + 1)

    header = "| {:^5} | {:^40} | {:^19} |".format("No", "Username", "Role")
    garis = "-"* 74


    print("-"*74)
    print(f"|{' ' * 72}|")
    print(f"|{'Daftar Akun':^72}|")
    print(f"|{' ' * 72}|")
    print("-"*74)

    print(garis)
    print(header)
    print(garis)

    for id, row in data_akun.iterrows():
        role = role_parse(row['Role'])
        print("| {:^5} | {:^40} | {:^19} |".format(id, row['Username'], role))
        print(garis)
    
    if msg:
        print(msg)
    
    if menu == "Perbarui":
        akun_diperbarui = input("Silahkan Masukkan Nomor Urut Dari Akun Yang Akan Diperbarui: ")
        
        if not akun_diperbarui.isdigit():
            daftar_akun(menu="Perbarui", msg="\nInput Harus Berupa Angka!\n", username=username)
        
        akun_diperbarui = data_akun.iloc[int(akun_diperbarui) - 1]
        
        if akun_diperbarui.empty:
            daftar_akun(menu="Hapus", msg="\nAkun Tersebut Tidak Ada Di Daftar Akun!\n", username=username)
        
        konfirmasi = menu_update(akun_diperbarui["Username"])
        daftar_akun(username=username)
        
    elif menu == "Hapus":
        akun_dihapus = input("Silahkan Masukkan Nomor Urut Dari Akun Yang Akan Dihapus: ")
        
        if not akun_dihapus.isdigit():
            daftar_akun("Hapus", "\nInput Harus Berupa Angka!\n", username=username)
        
        akun_dihapus = data_akun.iloc[int(akun_dihapus) - 1]
        
        if akun_dihapus.empty:
            daftar_akun("Hapus", "\nAkun Tersebut Tidak Ada Di Daftar Akun!\n", username=username)
        
        konfirmasi = hapus_akun(akun_dihapus["Username"])
        
        if konfirmasi:
            daftar_akun(msg="Akun Berhasil Dihapus!", username=username)
        else:
            daftar_akun(msg="Akun Batal Dihapus!", username=username)
        
    else:
        input("Tekan Enter Untuk Kembali...\n")
        return

def kelola_akun(errorMsg = False, username = False):
    os.system('cls')
    
    if errorMsg:
        print(errorMsg)
    
    print("Menu Kelola Akun\n1. Tambah Akun\n2. Lihat Daftar Akun\n3. Perbarui Data Akun\n4. Hapus Akun\n5. Kembali")
    menu_lanjutan = input("Silahkan Pilih Menu Berdasarkan Nomornya (1/2/3/4/5): ")
    
    if menu_lanjutan == "1":
        register(superAdmin=True)
        return kelola_akun(username=username)
    elif menu_lanjutan == "2":
        daftar_akun(username=username)
        return kelola_akun(username=username)
    elif menu_lanjutan == "3":
        daftar_akun(menu="Perbarui", username=username)
        return kelola_akun(username=username)
    elif menu_lanjutan == "4":
        daftar_akun(menu="Hapus", username=username)
        return kelola_akun(username=username)
    elif menu_lanjutan == "5":
        return
    else:
        return kelola_akun("Input Harus Berupa Nomor Sesuai Nomor Urut Menu!\n", username=username)
    
    
    
    