import os
import pandas as pd
from auth import login, register, role_parse
from lib import info_akun, daftarBarang, tambah_wishlist, lihat_wishlist, beli_barang, kelola

def menu_awal():
    while True:
        print("-"*80)
        print(f"|{' '*78}|")
        print(f"|{'SELAMAT DATANG DI TOKO PUPUK DAN ALAT TANI (SIJUPI)':^78}|")
        print(f"|{' '*78}|")
        print("-"*80)

        print(f"|{' ' * 78}|")
        print(f"|{'Kamu berada di menu tamu':^78}|")
        print(f"|{' ' * 78}|")
        print(f"|{'     1. Daftar Pupuk dan Alat Pertanian':<78}|")
        print(f"|{'     2. Menu Autentikasi':<78}|")
        print(f"|{'     3. Keluar':<78}|")
        print(f"|{' ' * 78}|")
        print("-" * 80)

        pilih_menu = input("Pilih berdasarkan nomor : ")
        
        match pilih_menu:
            case '1':
                os.system('cls')
                daftar_produk = pd.read_csv('db/products.csv')
                daftar_produk.index = daftar_produk.index + 1

                header = "| {:^5} | {:^28} | {:^10} | {:^15} | {:^5} |".format("No", "Nama Produk", "Jenis", "Harga", "Stok")
                garis = "-"* 79

                print(f"\n{'Daftar Pupuk dan Alat Pertanian':^80}\n")
                print(garis)
                print(header)
                print(garis)

                for id, row in daftar_produk.iterrows():
                    print("| {:^5} | {:<28} | {:>10} | {:>15} | {:>5} |".format(id, row['Nama Produk'], row['Jenis'], row['Harga'], row['Stock']))
                    print(garis)

                input("\nTekan Enter untuk kembali...")
                os.system('cls')
                continue
            case '2':
                menu_auth = menu_autentikasi()

                if len(menu_auth) == 2:
                    menu_utama(menu_auth)
                    return 'gas menu toko'
                elif menu_auth == 'keluar':
                    os.system('cls')
                    continue
            case '3':
                print('\nTerimakasih sudah berkunjung di toko kami 🙏')
                return 'keluar'
            case _:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue

def menu_autentikasi():
    os.system('cls')
    while True:
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'Kamu berada di menu autentikasi':^78}|")
        print(f"|{' ' * 78}|")
        print("-"*80)

        print(f"|{' ' * 78}|")
        print(f"|{'     1. Masuk ke akun':<78}|")
        print(f"|{'     2. Buat akun':<78}|")
        print(f"|{'     3. Kembali':<78}|")
        print(f"|{' ' * 78}|")
        print("-" * 80)

        pilih_auth = input("Pilih berdasarkan nomor : ")
        
        match pilih_auth:
            case '1':
                return login()
            case '2':
                return register()
            case '3':
                print('\nTerimakasih sudah berkunjung di toko kami 🙏')
                return 'keluar'
            case _:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue

def menu_utama(data_account):
    os.system('cls')

    account = data_account

    while True:
        print("-"*80)
        print(f"|{' ' * 78}|")
        print(f"|{'MENU TOKO SIJUPI':^78}|")
        print(f"|{' ' * 78}|")
        print(f"|{'Selamat datang ' + account[0] + '✨':^77}|")
        print(f"|{' ' * 78}|")
        print("-"*80)
        print(f"|     {'Berikut adalah daftar menu untuk ' + role_parse(account[1]) + '':<73}|")
        print(f"|{' ' * 78}|")

        if account[1] == 0:
            print(f"|{'     1. Kelola Pupuk dan Alat Tani':<78}|")
            print(f"|{'     2. Konfirmasi Pembelian':<78}|")
            print(f"|{'     3. Kelola Pembelian':<78}|")
            print(f"|{'     4. Kelola Pengeluaran Toko':<78}|")
            print(f"|{'     5. Laporan Penjualan dan Pengeluaran':<78}|")
            print(f"|{'     6. Lihat Notifikasi':<78}|")
            print(f"|{'     7. Kelola akun':<78}|")
            print(f"|{'     8. Perbarui Nomor Rekening Toko':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)
        
            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                kelola()
            elif pilih_menu == '2':
                print('konfir pembeli')
            elif pilih_menu == '3':
                print('kelola pembelian')
            elif pilih_menu == '4':
                print('kelola pengeluaran toko')
            elif pilih_menu == '5':
                print('laporan penjualan dan pengeluaran')
            elif pilih_menu == '6':
                print('lihat notif')
            elif pilih_menu == '7':
                print('kelola akun')
            elif pilih_menu == '8':
                print('update no rek')
            else:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue
            
        elif account[1] == 1:
            print(f"|{'     1. Kelola Pupuk dan Alat Tani':<78}|")
            print(f"|{'     2. Konfirmasi Pembelian':<78}|")
            print(f"|{'     3. Kelola Pembelian':<78}|")
            print(f"|{'     4. Kelola Pengeluaran Toko':<78}|")
            print(f"|{'     5. Laporan Penjualan dan Pengeluaran':<78}|")
            print(f"|{'     6. Lihat Notifikasi':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                kelola()
            elif pilih_menu == '2':
                print('konfir pembeli')
            elif pilih_menu == '3':
                print('kelola pembelian')
            elif pilih_menu == '4':
                print('kelola pengeluaran toko')
            elif pilih_menu == '5':
                print('laporan penjualan dan pengeluaran')
            elif pilih_menu == '6':
                print('lihat notif')
            else:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue

        elif account[1] == 2:
            print(f"|{'     1. Beli Pupuk dan Alat Pertanian':<78}|")
            print(f"|{'     2. Daftar Pembelian':<78}|")
            print(f"|{'     3. Info Akun':<78}|")
            print(f"|{'     4. Wishlist Produk':<78}|")
            print(f"|{'     5. Lihat Notifikasi':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                os.system('cls')
                while True:
                    lanjutanMenu = daftarBarang()
                    if lanjutanMenu == "1":
                        barang_mau_dibeli = beli_barang()
                        print(barang_mau_dibeli)
                    elif lanjutanMenu == "2":
                        tambah_wishlist(account[0])
                    elif lanjutanMenu == "3":
                        os.system('cls')
                        break
                    else:
                        os.system('cls')
                        print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                        continue
            elif pilih_menu == '2':
                print('daftar beli')
            elif pilih_menu == '3':
                account[0] = info_akun(account[0])
            elif pilih_menu == '4':
                lihat_wishlist(account[0])
            elif pilih_menu == '5':
                print('notif')
            else:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue
