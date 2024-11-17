import os
from menu import menu_autentikasi

def main():
    os.system('cls')
    print(f"{'SELAMAT DATANG DI TOKO PUPUK DAN ALAT TANI':^90}\n")

    menu_auth = menu_autentikasi()
    if len(menu_auth) == 2:
        print("MENU TOKO CUY")
    elif menu_auth == 'keluar':
        return 'keluar'

main()