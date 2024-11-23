import os
import pandas as pd
from auth import enkripsi_password, verifikasi_password
from auth import role_parse

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
