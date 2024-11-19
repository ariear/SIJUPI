import os
from auth import login, register

def menu_awal():
    while True:
        print("Kamu berada di menu tamu\n1. Daftar Pupuk dan Alat Pertanian\n2. Menu Autentikasi\n3. Keluar")
        pilih_menu = input("Pilih berdasarkan nomor : ")
        
        match pilih_menu:
            case '1':
                os.system('cls')
                print('gas daftar produk')
                return 'daftar produk'
            case '2':
                menu_auth = menu_autentikasi()

                if len(menu_auth) == 2:
                    print("MENU TOKO CUY")
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