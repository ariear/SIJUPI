import os
import pandas as pd
import csv
import random
from auth import enkripsi_password, verifikasi_password, daftar_huruf, register
from auth import role_parse
from datetime import datetime

# Fungsi untuk memformat sebuah angka menjadi bentuk rupiah
def format_rupiah(angka):
    return "Rp {:,}".format(angka).replace(",", ".")

# Fungsi untuk membaca informasi seputar toko
def baca_info_toko():
    toko = pd.read_csv('db/toko.csv')
    toko = toko.iloc[0]

    return toko

# Fungsi untuk menampilkan data produk
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
        print("| {:^5} | {:<29} | {:>10} | {:>15} | {:>5} |".format(id, row['Nama Produk'], row['Jenis'], format_rupiah(row['Harga']), row['Stock']))
        print(garis)


# Fungsi untuk mengelola produk (akses : admin dan pemilik toko)
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
            Nama = input("Nama Produk\t\t: ").strip()
            Nama_split = Nama.split(" ")
            
            if not Nama :
                print(f"\n{'⚠  Nama produk tidak boleh kosong ⚠':^78}\n")
                continue
            else : 
                alpha = True
                for kata in Nama_split :
                    if kata.isalpha() :
                        pass
                    else : 
                        print(f"\n{'⚠  Inputan hanya berupa huruf! ⚠':^78}\n")
                        alpha = False
                        break
                if not alpha :
                    Nama = None
                    continue
        
        if not Jenis:
            tipe = ["pupuk", "alat"]
            Jenis = input("Jenis (alat/pupuk)\t: ").strip()
            if Jenis in tipe : 
                if not Jenis:
                    print(f"\n{'⚠  Jenis produk tidak boleh kosong ⚠':^78}\n")
                    continue
            else :
                print(f"\n{'⚠  Jenis produk tidak sesuai ⚠':^78}\n")
                Jenis = None
                continue

        if Harga is None:
            Harga_input = input("Harga\t\t\t: ").strip()
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
            Stock_input = input("Stock\t\t\t: ").strip()
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

# Fungsi-fungsi untuk fitur notifikasi (akses : Pembeli)
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

def cek_notif_transaksi_admin(username):
    data_transaksi = pd.read_csv('db/transactions.csv')
    transaksi_belum_konfirmasi = len(data_transaksi[data_transaksi["Konfirmasi"].isnull()])
    notificationMsg([username], [f"Ada {transaksi_belum_konfirmasi} transaksi yang sedang menunggu konfirmasi!"])
    return

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

def update_wishlist(column = False, before = False, after = False):
    data_wishlist = pd.read_csv('db/wishlists.csv')
    if column == "Harga":
        data_wishlist.loc[data_wishlist["Nama Produk"] == before, "Harga"] = after
    else:
        data_wishlist.loc[data_wishlist[column] == before, column] = after
    data_wishlist.to_csv('db/wishlists.csv', index=False)

def update_produk(errorMsg=False):
    os.system('cls')

    if errorMsg:
        print(f"\n{errorMsg:^78}\n")

    daftarBarang()

    data = pd.read_csv('db/products.csv')
    data_wishlist = pd.read_csv('db/wishlists.csv')
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

            data_lama = data.loc[id_update]
            if choice == 1:
                Nama = input("Nama Produk Baru: ")
                if not Nama.strip():
                    os.system('cls')
                    print(f"\n{'Nama produk tidak boleh kosong! Coba lagi':^78}\n")
                    continue
                update_wishlist("Nama Produk", data_lama["Nama Produk"], Nama)
                pesanNotif = f"Produk {data_lama['Nama Produk']} telah diganti namanya menjadi {Nama}"
                data.loc[id_update, "Nama Produk"] = Nama

                os.system('cls')
                print(f"\n{'Nama produk berhasil diperbarui menjadi ' + Nama:^78}\n")
            elif choice == 2:
                Jenis = input("Jenis Baru: ")
                if not Jenis.strip():
                    os.system('cls')
                    print(f"\n{'Jenis produk tidak boleh kosong! Coba lagi':^78}\n")
                    continue
                pesanNotif = f"Produk {data_lama['Nama Produk']} telah diganti jenisnya menjadi {Jenis}"
                data.loc[id_update, "Jenis"] = Jenis

                os.system('cls')
                print(f"\n{'Jenis produk berhasil diperbarui menjadi ' + Jenis:^78}\n")
            elif choice == 3:
                try:
                    Harga = input("Harga Baru: ")
                    if not Harga.strip():
                        raise ValueError("Harga tidak boleh kosong!")
                    Harga = int(Harga)
                    update_wishlist("Harga", data.loc[id_update, "Nama Produk"], Harga)
                    pesanNotif = f"Produk {data_lama['Nama Produk']} harganya berubah menjadi {Harga}"
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
                    pesanNotif = f"Produk {data_lama['Nama Produk']} stocknya berubah menjadi {Stock}"
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

            data_username_wishlist = data_wishlist.loc[data_wishlist["Nama Produk"] == data_lama["Nama Produk"], "Username"].tolist()
            notificationMsg(data_username_wishlist, [pesanNotif])
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


# Fungsi untuk mengkonfirmasi pembelian (akses : admin dan pemilik toko)
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

            print(f"| {i:<5} {transaksi_id:<15} {group['Username'].iloc[0]:<20} {tanggal:<15} {format_rupiah(total_harga):<17} |")
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
                    
                    username = transaksi_df.loc[transaksi_df["Transaksi id"] == transaksi_id_pilih, "Username"].tolist()
                    notificationMsg(username, [f"selamat!! pembelian kamu dengan id {transaksi_id_pilih} sudah dikonfirmasi!!"])

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


# Fungsi untuk mengelola pembelian
def kelola_pembelian():
    os.system('cls')
    while True:
        transaksi_df = pd.read_csv('db/transactions.csv')

        if transaksi_df.empty:
            print("=" * 78)
            print(f"{'Tidak ada pembelian':^78}")
            print("=" * 78)
            input("\nTekan enter untuk kembali...")
            return

        print("-"*94)
        print(f"|{' ' * 92}|")
        print(f"|{'Daftar Pembelian':^92}|")
        print(f"|{' ' * 92}|")
        print("-"*94)

        print(f"| {'No':<5} {'Transaksi ID':<15} {'Nama Pembeli':<20} {'Tanggal':<15} {'Total Harga':<17} {'Status':<13} |")
        print("-" * 94)

        grouped_transaksi = transaksi_df.groupby("Transaksi id")
        daftar_transaksi = []
        for i, (transaksi_id, group) in enumerate(grouped_transaksi, start=1):
            total_harga = (group['Harga'] * group['Quantitas']).sum()
            daftar_transaksi.append(transaksi_id)
            tanggal = group['Tanggal Pembuatan'].iloc[0]
            status = "Lunas" if group['Lunas'].iloc[0] == True else "Belum Lunas"

            print(f"| {i:<5} {transaksi_id:<15} {group['Username'].iloc[0]:<20} {tanggal:<15} {format_rupiah(total_harga):<17} {status:<13} |")
        print("-" * 94)

        print("\nMenu:")
        print("1. Lihat detail pembelian")
        print("2. Ubah status pembelian")
        print("3. Hapus pembelian")
        print("4. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == '1':
            try:
                transaksi_pilihan = int(input("Pilih transaksi berdasarkan nomor : "))
                if 1 <= transaksi_pilihan <= len(daftar_transaksi):
                    transaksi_id = daftar_transaksi[transaksi_pilihan - 1]
                    transaksi_detail = transaksi_df[transaksi_df['Transaksi id'] == transaksi_id]
                    
                    os.system('cls')
                    print("=" * 78)
                    print(f"\n{'Struk Pembayaran':^78}\n")
                    print("=" * 78)
                    print(f"Transaksi ID : {transaksi_id}")
                    print(f"Username     : {transaksi_detail['Username'].iloc[0]}")
                    print(f"Tanggal      : {transaksi_detail['Tanggal Pembuatan'].iloc[0]}")
                    print(f"Metode Bayar : {transaksi_detail['Tipe Pembayaran'].iloc[0]}")
                    print("-" * 78)
                    print(f"{'Produk':<30} {'Harga':<15} {'Quantitas':<10} {'Subtotal':<15}")
                    print("-" * 78)
                    total_harga = 0
                    for _, row in transaksi_detail.iterrows():
                        subtotal = row['Harga'] * row['Quantitas']
                        total_harga += subtotal
                        print(f"{row['Nama Produk']:<30} {format_rupiah(row['Harga']):<15} {row['Quantitas']:<10} {format_rupiah(subtotal):<15}")
                    print("-" * 78)
                    print(f"{'Total Harga':>65}: {format_rupiah(total_harga)}")
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
        elif pilihan == '2':
            try:
                transaksi_pilihan = int(input("Pilih transaksi berdasarkan nomor (enter untuk batal): "))

                if 1 <= transaksi_pilihan <= len(daftar_transaksi):
                    transaksi_id = daftar_transaksi[transaksi_pilihan - 1]

                    status_pembelian = transaksi_df.loc[transaksi_df['Transaksi id'] == transaksi_id, 'Lunas'].iloc[0]

                    transaksi_df.loc[transaksi_df['Transaksi id'] == transaksi_id, 'Lunas'] = not status_pembelian
                    transaksi_df.to_csv('db/transactions.csv', index=False)

                    os.system('cls')
                    print(f"\n{'Status pembelian berhasil diubah!':^78}\n")
                else:
                    os.system('cls')
                    print(f"\n{'Transaksi tidak ada!! Pilih berdasarkan nomor!!':^78}")
            except ValueError:
                os.system('cls')
                print(f"\n{'Input harus berupa angka!':^78}")
        elif pilihan == '3':
            try:
                transaksi_pilihan = int(input("Pilih transaksi berdasarkan nomor (enter untuk batal): "))

                if 1 <= transaksi_pilihan <= len(daftar_transaksi):
                    transaksi_id = daftar_transaksi[transaksi_pilihan - 1]

                    konfirmasi = input(f"Apakah kamu yakin ingin menghapus transaksi dengan ID '{transaksi_id}'? (ya/tidak): ").strip().lower()
                    if konfirmasi == 'ya':
                        transaksi_df = transaksi_df[transaksi_df['Transaksi id'] != transaksi_id]
                        transaksi_df.to_csv('db/transactions.csv', index=False)

                        os.system('cls')
                        print(f"\n{'Transaksi berhasil dihapus!':^78}\n")
                    elif konfirmasi == 'tidak':
                        os.system('cls')
                        print(f"\n{'Transaksi batal dihapus.':^78}\n")
                    else:
                        os.system('cls')
                        print(f"\n{'Input tidak valid. Pilih antara ya atau tidak.':^78}\n")
                else:
                    os.system('cls')
                    print(f"\n{'Transaksi tidak ada!! Pilih berdasarkan nomor!!':^78}")
            except ValueError:
                os.system('cls')
                print(f"\n{'Input harus berupa angka!':^78}")
        elif pilihan == '4':
            os.system('cls')
            return
        else:
            os.system('cls')
            print(f"\n{'⚠  Pilih menu berdasarkan nomor!! ⚠':^78}\n")
            continue


#Fungsi untuk mengelola pengeluaran
def daftar_pengeluaran():
    pengeluaran = pd.read_csv('db/pengeluaran.csv')
    pengeluaran.index = pengeluaran.index + 1

    header = "| {:^5} | {:<22} | {:>10} | {:>15} | {:>10} | {:>22} |".format('No', 'Nama Barang', 'Jumlah', 'Harga', 'Total', 'Tanggal')
    garis = "-"* 105


    print("-"*105)
    print(f"|{' ' * 103}|")
    print(f"|{'Daftar Pengeluaran Toko':^103}|")
    print(f"|{' ' * 103}|")
    print("-"*105)

    print(garis)
    print(header)
    print(garis)

    for id, row in pengeluaran.iterrows():
        print("| {:^5} | {:<22} | {:>10} | {:>15} | {:>10} | {:>22} |".format(id, row['Nama Barang'], row['Jumlah'], format_rupiah(row['Harga']), format_rupiah(row['Total']), row['Tanggal']))
        print(garis)
        
def kelola_pengeluaran() :
    os.system('cls')
    while True:
        daftar_pengeluaran()

        print("Menu:")
        print("1. Tambah Data")
        print("2. Update Data")
        print("3. Hapus Data")
        print("4. Keluar")
        choice = input("Pilih opsi: ")
        os.system('cls')

        if choice == '1':
            tambah_pengeluaran()
        elif choice == '2':
            update_pengeluaran()
        elif choice == '3':
            hapus_pengeluaran()
        elif choice == '4':
            break
        else:
            print(f"\n{'⚠  Masukkan nomor yang valid! ⚠':^78}\n")

def tambah_pengeluaran():
    if not os.path.exists('db/pengeluaran.csv'):
        with open('db/pengeluaran.csv', mode='w', newline='') as file :
            csv_writer = csv.writer(file)
            header = ('Nama Barang', 'Jumlah', 'Harga', 'Total', 'Tanggal')
            csv_writer.writerow(header)

    print("-" * 105)
    print(f"|{' ' * 103}|")
    print(f"|{'TAMBAH pengeluaran':^103}|")
    print(f"|{' ' * 103}|")
    print("-" * 105)

    Nama, Jumlah, Harga, Total, Tanggal = None, None, None, None, None
    while True:
        if not Nama:
            Nama = input("Nama pengeluaran\t\t: ").strip()
            Nama_split = Nama.split(" ")
            
            if not Nama :
                print(f"\n{'⚠  Nama pengeluaran tidak boleh kosong ⚠':^78}\n")
                continue
            else : 
                alpha = True
                for kata in Nama_split :
                    if kata.isalpha() :
                        pass
                    else : 
                        print(f"\n{'⚠  Inputan hanya berupa huruf! ⚠':^78}\n")
                        alpha = False
                        break
                if not alpha :
                    Nama = None
                    continue
                
        if Jumlah is None:
            Jumlah_input = input("Jumlah\t\t\t: ").strip()
            try:
                Jumlah = int(Jumlah_input)
                if Jumlah < 0:
                    print(f"\n{'⚠  Jumlah harus berupa angka positif ⚠':^78}\n")
                    Jumlah = None
                    continue
            except ValueError:
                print(f"\n{'⚠  Jumlah harus berupa angka ⚠':^78}\n")
                continue

        if Harga is None:
            Harga_input = input("Harga\t\t\t: ").strip()
            try:
                Harga = int(Harga_input)
                if Harga < 0:
                    print(f"\n{'⚠  Harga harus berupa angka positif ⚠':^78}\n")
                    Harga = None
                    continue
            except ValueError:
                print(f"\n{'⚠  Harga harus berupa angka ⚠':^78}\n")
                continue

        if Total is None:
            Total = Jumlah * Harga
            
        if Tanggal is None :
            Tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if Nama and Jumlah and Harga is not None and Total is not None and Tanggal is not None:
            break
    
    with open('db/pengeluaran.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow((Nama, Jumlah, Harga, Total, Tanggal))
    
    os.system('cls')
    print(f"\n{'pengeluaran berhasil ditambahkan!!':^78}\n")


def update_pengeluaran():
    os.system('cls')
    daftar_pengeluaran()
    
    data = pd.read_csv('db/pengeluaran.csv')
    data.index = data.index + 1
        
    try:
        id_update = int(input("\nPilih pengeluaran untuk diperbarui berdasarkan nomor : "))
    except ValueError:
        print("Input harus berupa angka!")
        return
    
    if id_update in data.index:
        os.system('cls')
        while True:
            print(f"\n{'Pengeluaran terpilih: ' + data.loc[id_update, 'Nama Barang']:^78}")
            print("\nPilih data yang ingin diperbarui :")
            print("1. Ubah Nama Barang")
            print("2. Ubah Jumlah")
            print("3. Ubah Harga")
            print("4. Ubah Waktu")
            print("5. Batal")
            try:
                choice = int(input("\nPilih berdasarkan nomor : "))
            except ValueError:
                os.system('cls')
                print(f"\n{'Input harus berupa angka! Coba lagi':^78}\n")
                continue

            if choice == 1:
                Nama = input("Nama Barang Baru: ")
                if not Nama.strip():
                    os.system('cls')
                    print(f"\n{'Nama barang tidak boleh kosong! Coba lagi':^78}\n")
                    continue
                
                data.loc[id_update, "Nama Barang"] = Nama

                os.system('cls')
                print(f"\n{'Nama barang berhasil diperbarui menjadi ' + Nama:^78}\n")
                
                
            elif choice == 2:
                try:
                    Jumlah = input("Jumlah Baru: ")
                    if not Jumlah.strip():
                        raise ValueError("Jumlah tidak boleh kosong!")
                    Jumlah = int(Jumlah)
                    data.loc[id_update, "Jumlah"] = Jumlah
                    data.loc[id_update, "Total"] = data.loc[id_update, "Harga"] * Jumlah
                    os.system('cls')
                    print(f"\n{'Jumlah produk berhasil diperbarui menjadi ' + str(Jumlah):^78}\n")
                except ValueError:
                    os.system('cls')
                    print(f"\n{'Jumlah harus berupa angka! Coba lagi':^78}\n")
                    continue
    
    
            elif choice == 3:
                try:
                    Harga = input("Harga Baru: ")
                    if not Harga.strip():
                        raise ValueError("Harga tidak boleh kosong!")
                    Harga = int(Harga)
                    data.loc[id_update, "Harga"] = Harga
                    data.loc[id_update, "Total"] = data.loc[id_update, "Jumlah"] * Harga
                    os.system('cls')
                    print(f"\n{'Harga produk berhasil diperbarui menjadi ' + str(Harga):^78}\n")
                except ValueError:
                        os.system('cls')
                        print(f"\n{'Harga harus berupa angka! Coba lagi':^78}\n")
              
            elif choice == 4 :
                jawab = ["iya", "tidak"]
                Tanggal = input("Apakah anda ingin memperbarui waktu?(iya/tidak) : ")
                if Tanggal in jawab :
                    if Tanggal == "iya" :
                        Tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    else :
                            print("Silahkan pilih menu lainnya")
                else :
                    print("Masukkan jawaban dengan benar!")
                data.loc[id_update, "Tanggal"] = Tanggal
                
            elif choice == 5:
                os.system('cls')
                return
            else:
                os.system('cls')
                print(f"\n{'Pilih berdasarkan nomor menu!!':^78}\n")
                continue

            data.to_csv('db/pengeluaran.csv', index=False)
            return
    else:
        os.system('cls')
        print(f"Produk yang kamu pilih tidak ada!")
        return

def hapus_pengeluaran() :
    while True:
        daftar_pengeluaran()

        data = pd.read_csv('db/pengeluaran.csv')
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
                        data.to_csv('db/pengeluaran.csv', index=False)
                        
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

#Fungsi untuk menampilkan laporan
def laporan() :
    os.system('cls')
    while True:
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'Laporan Penjualan dan Pengeluaran':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)

        print("\nMenu:")
        print("1. Laporan Penjualan")
        print("2. Laporan Pengeluaran")
        print("3. Keluar")
        choice = input("Pilih opsi: ")
        os.system('cls')

        if choice == '1':
            lap_penjualan()
        elif choice == '2':
            lap_pengeluaran()
        elif choice == '3':
            break
        else:
            print(f"\n{'⚠  Masukkan nomor yang valid! ⚠':^78}\n")
            
def lap_penjualan():
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'Laporan Penjualan':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    awal = input("Masukkan tanggal awal (DD-MM-YYYY)\t: ")
    akhir = input("Masukkan tanggal akhir (DD-MM-YYYY)\t: ")
    
    try:
        tanggal_awal = datetime.strptime(awal, "%d-%m-%Y").date()
        tanggal_akhir = datetime.strptime(akhir, "%d-%m-%Y").date()
        if tanggal_awal > tanggal_akhir:
            os.system('cls')
            print("⚠ Tanggal awal tidak boleh lebih besar dari tanggal akhir! ⚠")
            return

        data = pd.read_csv('db/transactions.csv')
        data['Tanggal Pembuatan'] = pd.to_datetime(data['Tanggal Pembuatan'], format='%d-%m-%Y', errors='coerce')
        laporan = data[(data['Tanggal Pembuatan'].dt.date >= tanggal_awal) & 
                       (data['Tanggal Pembuatan'].dt.date <= tanggal_akhir)]
        
        if laporan.empty:
            os.system('cls')
            print(f"⚠ Tidak ada transaksi antara tanggal {tanggal_awal} dan {tanggal_akhir} ⚠")
            return

        os.system('cls')
        print("=" * 115)
        print(f"\n{'Laporan Penjualan':^115}\n")
        print("=" * 115)
        print(f"\nRentang Tanggal: {tanggal_awal} hingga {tanggal_akhir}\n")
        print("-" * 115)
        print(f"{'Transaksi ID':<15} {'Username':<15} {'Nama Produk':<30} {'Harga':<10} {'Quantitas':<10} {'Total':<12} {'Tipe Pembayaran':<15}")
        print("-" * 115)

        total = 0
        for index, row in laporan.iterrows():
            hasil = row['Harga'] * row['Quantitas']
            total += hasil
            print(f"{row['Transaksi id']:<15} {row['Username']:<15} {row['Nama Produk']:<30} {format_rupiah(row['Harga']):<10} {row['Quantitas']:<10} {format_rupiah(hasil):<12} {row['Tipe Pembayaran']:<15}")

        print("-" * 115)
        print(f"{'Total Harga':>75}: {format_rupiah(total)}")
        print("=" * 115)

        input("Tekan enter untuk kembali....")
        os.system('cls')
    except ValueError:
        print("⚠ Format tanggal tidak valid. Harap masukkan dalam format DD-MM-YYYY! ⚠")
        os.system('cls')

def lap_pengeluaran():
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'Laporan Pengeluaran':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    awal = input("Masukkan tanggal awal (DD-MM-YYYY)\t: ")
    akhir = input("Masukkan tanggal akhir (DD-MM-YYYY)\t: ")
    
    try:
        tanggal_awal = datetime.strptime(awal, "%d-%m-%Y")
        tanggal_akhir = datetime.strptime(akhir, "%d-%m-%Y")
        if tanggal_awal > tanggal_akhir:
            os.system('cls')
            print("⚠ Tanggal awal tidak boleh lebih besar dari tanggal akhir! ⚠")
            return
        data = pd.read_csv('db/pengeluaran.csv')
        data.index = data.index + 1
        data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        laporan = data[(data['Tanggal'] >= tanggal_awal) & 
                       (data['Tanggal'] <= tanggal_akhir)]
        
        if laporan.empty:
            os.system('cls')
            print(f"⚠ Tidak ada pengeluaran antara tanggal {tanggal_awal.date()} dan {tanggal_akhir.date()} ⚠")
            return
        
        os.system('cls')
        print("=" * 90)
        print(f"\n{'Laporan Pengeluaran':^90}\n")
        print("=" * 90)
        print(f"\nRentang Tanggal: {tanggal_awal.date()} hingga {tanggal_akhir.date()}\n")
        print("-" * 90)
        print(f"{'Nama Barang':<30} {'Jumlah':<10} {'Harga':<10} {'Total':<15} {'Tanggal':<25}")
        print("-" * 90)
        total_akhir = 0
        for index, row in laporan.iterrows():
            hasil = row['Harga'] * row['Jumlah']
            total_akhir += hasil
            print(f"{row['Nama Barang']:<30} {row['Jumlah']:<10} {format_rupiah(row['Harga']):<10} {format_rupiah(row['Total']):<15} {row['Tanggal']}")
        print("-" * 90)
        print(f"{'Total Harga':>65}: {format_rupiah(total_akhir)}")
        print("=" * 90)

        input("Tekan enter untuk kembali....")
        os.system('cls')
    except ValueError:
        print("⚠ Format tanggal tidak valid. Harap masukkan dalam format DD-MM-YYYY! ⚠")
        os.system('cls')
        

# Fungsi untuk mengelola akun (akses : Pemilik toko)
def kelola_akun(errorMsg = False, username = False):
    os.system('cls')
    
    if errorMsg:
        print(f"\n{errorMsg:^78}")
    
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'Menu Kelola Akun':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)

    print("Menu :\n1. Tambah Akun\n2. Lihat Daftar Akun\n3. Perbarui Data Akun\n4. Hapus Akun\n5. Kembali")
    menu_lanjutan = input("Pilih Menu Berdasarkan Nomor (1/2/3/4/5): ")
    
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
        os.system('cls')
        return
    else:
        return kelola_akun("Input Harus Berupa Nomor Sesuai Nomor Urut Menu!\n", username=username)
    

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
        print(f"{msg:^78}")
    
    if menu == "Perbarui":
        akun_diperbarui = input("Silahkan Masukkan Nomor Urut Dari Akun Yang Akan Diperbarui: ")
        
        if not akun_diperbarui.isdigit() or int(akun_diperbarui) not in data_akun.index:
            daftar_akun(menu="Perbarui", msg="\nInput Harus Berupa Angka!\n", username=username)
        
        akun_diperbarui = data_akun.iloc[int(akun_diperbarui) - 1]
        
        if akun_diperbarui.empty:
            daftar_akun(menu="Hapus", msg="\nAkun Tersebut Tidak Ada Di Daftar Akun!\n", username=username)
        
        konfirmasi = menu_update(akun_diperbarui["Username"])
        daftar_akun(username=username)
        
    elif menu == "Hapus":
        akun_dihapus = input("Silahkan Masukkan Nomor Urut Dari Akun Yang Akan Dihapus: ")
        
        if not akun_dihapus.isdigit() or int(akun_dihapus) not in data_akun.index:
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
        input("Tekan Enter Untuk Kembali...")
        return
    
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



# Fungsi untuk memperbarui informasi seputar toko (akses : Pemilik Toko)
def update_info_toko():
    os.system('cls')
    data_toko = pd.read_csv('db/toko.csv')
    data_toko = data_toko.iloc[0]
    while True:
        print("-"*74)
        print(f"|{' ' * 72}|")
        print(f"|{'Perbarui Informasi Toko':^72}|")
        print(f"|{' ' * 72}|")
        print("-"*74)

        print(f"|    {'Nama Toko      : ' + data_toko['Nama Toko']:<68}|")
        print(f"|    {'Nomor Rekening : ' + str(data_toko['No Rek']):<68}|")
        print(f"|    {'Nomor whatsapp : ' + str(data_toko['No Wa']):<68}|")
        print("-"*74)

        print("\nMenu :")
        print("1. Perbarui nama toko")
        print("2. Perbarui nomor rekening toko")
        print("3. Perbarui nomor whatsapp")
        print("4. Kembali")

        pilih_menu = input("\nPiih menu berdasarkan nomor : ")

        if pilih_menu == "1":
            nama_baru = input("Masukkan nama toko baru: ").strip()
            if nama_baru:
                data_toko['Nama Toko'] = nama_baru
                break
            else:
                os.system('cls')
                print(f"\n{'⚠  Nama toko tidak boleh kosong. Silakan masukkan kembali. ⚠':^78}\n")
                continue

        elif pilih_menu == "2":
            rekening_baru = input("Masukkan nomor rekening baru: ").strip()
            if rekening_baru:
                data_toko['No Rek'] = rekening_baru
                break
            else:
                os.system('cls')
                print(f"\n{'⚠  Nomor rekening tidak boleh kosong. Silakan masukkan kembali. ⚠':^78}\n")
                continue

        elif pilih_menu == "3":
            wa_baru = input("Masukkan nomor WhatsApp baru: ").strip()
            if wa_baru:
                data_toko['No Wa'] = wa_baru
                break
            else:
                os.system('cls')
                print(f"\n{'⚠  Nomor WhatsApp tidak boleh kosong. Silakan masukkan kembali. ⚠':^78}\n")
                continue
        elif pilih_menu == "4":
            os.system('cls')
            return
        else:
            os.system('cls')
            print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
            continue

    data_toko.to_frame().T.to_csv('db/toko.csv', index=False)
    update_info_toko()


# Fungsi untuk melihat informasi seputar akun yang login (akses : Pembeli, Admin, Pemilik Toko)
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

# Fungsi untuk membeli produk (akses : pembeli)
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
                                    sisa = stock - qty
                                    barang_fix.append(nama_produk)
                                    quantitas.append(qty)
                                    daftar_harga.append(harga)

                                    df.loc[pilihan-1, 'Stock'] = sisa
                                    if (sisa) <= 3:
                                        data_akun = pd.read_csv('db/accounts.csv')
                                        data_akun_admin = data_akun.loc[data_akun["Role"] == 1, "Username"].to_list()
                                        data_akun_pemilik = data_akun.loc[data_akun["Role"] == 0, "Username"].to_list()
                                        
                                        penerima = data_akun_pemilik + data_akun_admin
                                        notificationMsg(penerima, [f"Stock dari {nama_produk} sudah mau habis! tersisa: {sisa} stock!"])

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
                    continue
            except ValueError:
                print("\nInput harus berupa angka!")
                continue
            
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
            print(f"{nama:<30} {format_rupiah(harga):<15} {qty:<10} {format_rupiah(subtotal):<15}")
        print("-" * 78)
        print(f"{'Total Harga':>65}: {format_rupiah(total_harga)}")
        print("=" * 78)

        if bayar == "Transfer":
            toko = baca_info_toko()

            print("\nSilahkan transfer ke rekening berikut untuk menyelesaikan transaksi:")
            print(f"Bank BRI, No. Rekening: {toko['No Rek']}, a.n. {toko['Nama Toko']}\n")

            print(f"\nKonfirmasi pembayaran melalui nomor berikut : {toko['No Wa']}\n")
            print("=" * 78)
        
        return input('Tekan enter untuk keluar.....')
    

# Fungsi untuk menambah wishlist (akses : Pembeli)
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


# Fungsi untuk melihat daftar transaksi
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

            print(f"| {i:<5} {transaksi_id:<15} {tanggal:<15} {format_rupiah(total_harga):<18} {status:<20}|")
        
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
                        print(f"{row['Nama Produk']:<30} {format_rupiah(row['Harga']):<15} {row['Quantitas']:<10} {format_rupiah(subtotal):<15}")
                    print("-" * 78)
                    print(f"{'Total Harga':>65}: {format_rupiah(total_harga)}")
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


# Fungsi untuk melihat daftar wishlist (akses : pembeli)
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
                print("| {:^5} | {:<28} | {:>37} |".format(id, row['Nama Produk'], format_rupiah(row['Harga'])))
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
