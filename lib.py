import os
import pandas as pd
import csv
import random
from auth import enkripsi_password, verifikasi_password, daftar_huruf
from auth import role_parse
from datetime import datetime
import pytz

time_zone = pytz.timezone("Asia/Jakarta")

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

def notificationMsg(penerima = False, pesan = False):
    if penerima and pesan:
        data_notif = pd.read_csv('db/notifications.csv')
        
        data_baru_list = []
        for topik in pesan:
            for akun in penerima:
                data_baru_list.append({
                    "Username": akun,
                    "Deskripsi": topik,
                    "Tanggal": datetime.now(time_zone).strftime("%Y-%m-%d"),
                    "Terbaca": False
                })
        
        data_baru = pd.DataFrame(data_baru_list)
        
        data_notif = pd.concat([data_notif, data_baru], ignore_index=True)
        
        data_notif.to_csv("db/notifications.csv", index=False)
    return

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

def update(errorMsg = False):
    os.system('cls')
    
    if errorMsg:
        print(errorMsg)
        
    data = pd.read_csv('db/products.csv')
    data.index = data.index + 1
    print(data)
        
    id_update = int(input("Masukkan ID yang ingin diupdate : ")) - 1
    if (id_update + 1) in data.index:
        Nama = input("Nama Produk\t: ")
        Jenis = input("Jenis\t: ")                
        Harga = int(input("Harga\t: "))
        Stock = int(input("Stock\t: "))
        
        nama_awal, jenis_awal, harga_awal, stock_awal = data.loc[(id_update + 1), ["Nama Produk", "Jenis", "Harga", "Stock"]]
        
        data.iloc[id_update] = [Nama, Jenis, Harga, Stock]
        data.to_csv('db/products.csv', index=False)
        
        wishlistData = pd.read_csv('db/wishlists.csv')
        filteredWishlist = wishlistData[wishlistData["Nama Produk"] == nama_awal ]
        
        if not filteredWishlist.empty:
            username_list = filteredWishlist["Username"].tolist()
            pesan = []
            if Nama != nama_awal:
                pesan.append(f"{nama_awal} telah diganti namanya menjadi {Nama}")
                update_wishlist("Nama Produk", nama_awal, Nama)
            if Jenis != jenis_awal:
                pesan.append(f"Jenis barang dari {Nama} telah diganti menjadi Rp. {Jenis}")
            if Harga != harga_awal:
                pesan.append(f"Harga {Nama} telah diubah menjadi {Harga:,}")
                update_wishlist("Harga", harga_awal, Harga)
            if Stock != stock_awal:
                pesan.append(f"Stock {Nama} sekarang adalah {Stock}")
            notificationMsg(username_list, pesan)
            
        os.system('cls')
        print("Data telah diupdate!")
        print(data)
    else:
        update(f"Barang dengan ID {id_update + 1} tidak ada!")
        return
    return
    
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
        
def notif_sudah_terbaca(username = False):
    os.system('cls')
    notif = pd.read_csv("db/notifications.csv")
    notif = notif[(notif["Username"] == username) & (notif["Terbaca"] == True)]
    notif = notif[["Deskripsi", "Tanggal"]]
    notifikasi = notif.values.tolist()

    print("{:^20}  {:} \n".format("Tanggal", "Deskripsi"))
    for item in notifikasi:
        print(f"{item[1]:^20}{item[0]}\n")
    input("Tekan Enter Untuk Kembali...")
    return

def notif_belum_terbaca(username = False):
    os.system('cls')
    notif = pd.read_csv("db/notifications.csv")
    notif = notif[(notif["Username"] == username) & (notif["Terbaca"] == False)]
    if not notif.empty:
        tampilkan_notif = notif[["Deskripsi", "Tanggal"]]
        notifikasi = tampilkan_notif.values.tolist()

        print("{:^20}  {:} \n".format("Tanggal", "Deskripsi"))
        for item in notifikasi:
            print(f"{item[1]:^20}{item[0]}\n")
            
        notif["Terbaca"] = True
        notif.to_csv('db/notifications.csv', index=False)
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
