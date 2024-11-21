import os
import pandas as pd
from auth import login, register, role_parse

def menu_awal():
    while True:
        print(f"\n{'SELAMAT DATANG DI TOKO PUPUK DAN ALAT TANI (SIJUPI)':^90}\n")
        print("Kamu berada di menu tamu\n1. Daftar Pupuk dan Alat Pertanian\n2. Menu Autentikasi\n3. Keluar")
        pilih_menu = input("Pilih berdasarkan nomor : ")
        
        match pilih_menu:
            case '1':
                os.system('cls')
                daftar_produk = pd.read_csv('db/products.csv')
                daftar_produk.index = daftar_produk.index + 1
                print(f"\n{'Daftar Pupuk dan Alat Pertanian':^40}\n")
                print(daftar_produk)

                input("\nKetik apapun untuk kembali ke menu : ")
                os.system('cls')
                continue
            case '2':
                menu_auth = menu_autentikasi()

                if len(menu_auth) == 2:
                    menu_utama(menu_auth)
                    return 'gas menu toko'
                elif menu_auth == 'keluar':
                    return 'keluar'
            case '3':
                print('\nTerimakasih sudah berkunjung di toko kami 🙏')
                return 'keluar'
            case _:
                os.system('cls')
                print('\nInput harus ada di menu dan berupa angka!\n')
                continue

def menu_autentikasi():
    os.system('cls')
    while True:
        print("Kamu berada di menu autentikasi")
        print("1. Masuk ke akun\n2. Buat akun\n3. Keluar\n")
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
                print('\nInput harus ada di menu dan berupa angka!\n')
                continue

def menu_utama(data_account):
    os.system('cls')

    account = data_account

    while True:
        print(f"\n{'MENU TOKO SIJUPI':^50}\n\nSelamat datang {account[0]}✨\n\nBerikut adalah daftar menu untuk {role_parse(account[1])}")

        if account[1] == 0:
            print("1. Kelola Pupuk dan Alat Tani\n2. Konfirmasi Pembelian\n3. Kelola Pembelian\n4. Kelola Pengeluaran Toko\n5. Laporan Penjualan dan Pengeluaran\n6. Lihat Notifikasi\n7. Kelola akun\n8. Perbarui Nomor Rekening Toko")
        
            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                print('kelola pupuk ')
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
                print('Input harus ada di menu dan berupa angka!')
                continue
        elif account[1] == 1:
            print("1. Kelola Pupuk dan Alat Tani\n2. Konfirmasi Pembelian\n3. Kelola Pembelian\n4. Kelola Pengeluaran Toko\n5. Laporan Penjualan dan Pengeluaran\n6. Lihat Notifikasi")

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                print('kelola pupuk ')
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
                print('Input harus ada di menu dan berupa angka!')
                continue
        elif account[1] == 2:
            print("1. Beli Pupuk dan Alat Pertanian\n2. Daftar Pembelian\n3. Info Akun\n4. Wishlist Barang\n5. Lihat Notifikasi")

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                print('beli pupuk ')
            elif pilih_menu == '2':
                print('daftar beli')
            elif pilih_menu == '3':
                print('info akun')
            elif pilih_menu == '4':
                print('wislis')
            elif pilih_menu == '5':
                print('notif')
            else:
                os.system('cls')
                print('Input harus ada di menu dan berupa angka!')
                continue
