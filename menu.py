import os
from auth import login, register, role_parse
from lib import info_akun, daftarBarang, tambah_wishlist, lihat_wishlist, beli_barang, kelola_produk, daftar_transaksi, notifikasi, konfirmasi_pembelian, kelola_pengeluaran, laporan, kelola_akun, update_info_toko, cek_notif_transaksi_admin

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
                daftarBarang()

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
                print(f"\n{'Terimakasih sudah berkunjung di toko kami 🙏':^78}")
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
                os.system('cls')
                return 'kembali'
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
            print(f"|{'     9. Info Akun':<78}|")
            print(f"|{'     10. Logout':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)
        
            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                kelola_produk()
            elif pilih_menu == '2':
                konfirmasi_pembelian()
            elif pilih_menu == '3':
                print('kelola pembelian')
            elif pilih_menu == '4':
                kelola_pengeluaran()
            elif pilih_menu == '5':
                print('laporan penjualan dan pengeluaran')
            elif pilih_menu == '6':
                cek_notif_transaksi_admin(account[0])
                notifikasi(account[0])
            elif pilih_menu == '7':
                kelola_akun(username=account[0])
            elif pilih_menu == '8':
                update_info_toko()
            elif pilih_menu == '9':
                account[0] = info_akun(account[0])
            elif pilih_menu == '10':
                print(f"\n{'Terimakasih sudah berkunjung di toko kami 🙏':^78}")
                return True
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
            print(f"|{'     7. Info Akun':<78}|")
            print(f"|{'     8. Logout':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                kelola_produk()
            elif pilih_menu == '2':
                konfirmasi_pembelian()
            elif pilih_menu == '3':
                print('kelola pembelian')
            elif pilih_menu == '4':
                kelola_pengeluaran()
            elif pilih_menu == '5':
                laporan()
            elif pilih_menu == '6':
                cek_notif_transaksi_admin(account[0])
                notifikasi(account[0])
            elif pilih_menu == '7':
                account[0] = info_akun(account[0])
            elif pilih_menu == '8':
                print(f"\n{'Terimakasih sudah berkunjung di toko kami 🙏':^78}")
                return True
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
            print(f"|{'     6. Logout':<78}|")
            print(f"|{' ' * 78}|")
            print("-" * 80)

            pilih_menu = input("Pilih berdasarkan nomor : ")
            if pilih_menu == '1':
                os.system('cls')
                while True:
                    daftarBarang()

                    print(f"|{' ' * 78}|")
                    print(f"|{'     Daftar Menu:':<78}|")
                    print(f"|{'     1. Beli Produk':<78}|")
                    print(f"|{'     2. Tambah Wishlist Produk':<78}|")
                    print(f"|{'     3. Kembali':<78}|")
                    print(f"|{' ' * 78}|")
                    print("-" * 80)

                    lanjutanMenu = input("\nPilih berdasarkan nomor menu : ")
                    if lanjutanMenu == "1":
                        beli_barang(account[0])
                        os.system('cls')
                        continue
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
                daftar_transaksi(account[0])
            elif pilih_menu == '3':
                account[0] = info_akun(account[0])
            elif pilih_menu == '4':
                lihat_wishlist(account[0])
            elif pilih_menu == '5':
                notifikasi(account[0])
            elif pilih_menu == '6':
                print(f"\n{'Terimakasih sudah berkunjung di toko kami 🙏':^78}")
                return True
            else:
                os.system('cls')
                print(f"\n{'⚠  Input harus ada di menu dan berupa angka! ⚠':^78}\n")
                continue
