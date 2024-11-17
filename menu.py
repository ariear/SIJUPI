import os
from auth import login, register

def menu_autentikasi():
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