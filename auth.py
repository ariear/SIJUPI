import os
import pandas as pd
import random

def accountData():
    return pd.read_csv('db/accounts.csv')

def login(errorMsg = False):
    os.system('cls')
    
    if errorMsg:
        print(f"\n{' ' * 10} {errorMsg} ❌\n")
        
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'LOGIN':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)
    
    while True:
        username = input("\n🙍 Masukkan Username anda: ")
        password = input("🔑 Masukkan Password anda: ")
        
        accounts = accountData()
        
        account = accounts[accounts['Username'] == username]
            
        if account.empty:
            return login("Maaf Username Atau Password Yang Anda Berikan Salah!")
        
        if account["Password"].isnull().any():
            register(resetPassword=username)
        elif not verifikasi_password(account.iloc[0]["Password"], password):
            return login("Maaf Username Atau Password Yang Anda Berikan Salah!")
        
        break
    
    return [account.iloc[0]["Username"], account.iloc[0]["Role"]]


def addAccount(username = None, password = None, role = None, resetPassword = False):
    password = enkripsi_password(password)
    
    if resetPassword:
        data_akun = pd.read_csv('db/accounts.csv')
        data_akun.loc[data_akun["Username"] == resetPassword, "Password"] = password
        
        data_akun.to_csv('db/accounts.csv')
        return
    
    if role is None:
        role = 2
    
    new_account = pd.DataFrame({
        'Username': [username],
        'Password': [password],
        'Role': [role]
    })
    new_account.to_csv('db/accounts.csv', mode='a', header=False, index=False)
    
    return [username, role]

def register(errorMsg = False, superAdmin = False, resetPassword = False):
    if resetPassword:
        if errorMsg:
            print(f"\n{' ' * 10} {errorMsg} ❌\n")
        
        print("Password anda telah di reset oleh pemilik toko, silahkan masukkan password baru!")
        password = input("🔑 Masukkan Password Baru (minimal 8 character!): ").strip()
        confirmedPassword = input("🔐 Konfirmasi Ulang Password: ").strip()
        
        if not password:
            return register(errorMsg="Password tidak boleh hanya berupa spasi!", resetPassword=resetPassword)
        
        if len(password) < 8:
            return register(errorMsg="Password Akun Minimal 8 character!", resetPassword=resetPassword)
        
        if password != confirmedPassword:
            return register(errorMsg="Konfirmasi Ulang Password Berbeda Dengan Password Awal!", resetPassword=resetPassword)
        return addAccount(password=password, resetPassword=resetPassword)
    
    os.system('cls')
    
    if errorMsg:
        print(f"\n{' ' * 10} {errorMsg} ❌\n")
        
    print("-"*80)
    print(f"|{' ' * 78}|")
    print(f"|{'REGISTER':^78}|")
    print(f"|{' ' * 78}|")
    print("-"*80)
    
    while True:
        username = input("\n🙍 Masukkan Username (minimal 3 character!): ").strip()
        password = input("🔑 Masukkan Password (minimal 8 character!): ").strip()
        confirmedPassword = input("🔐 Konfirmasi Ulang Password: ").strip()
        role = None

        if not username:
            return register("Username tidak boleh hanya berupa spasi!")
        
        if len(username) < 3:
            return register("Username Akun Minimal 3 character!")
            
        accounts = accountData()
        
        if not accounts[accounts['Username'] == username].empty:
            return register("Username Sudah Digunakan!")
        
        if not password:
            return register("Password tidak boleh hanya berupa spasi!")

        if len(password) < 8:
            return register("Password Akun Minimal 8 character!")
        
        if password != confirmedPassword:
            return register("Konfirmasi Ulang Password Berbeda Dengan Password Awal!")
        
        if superAdmin:
            while True:
                print("\n🎟  ROLE:"
                    +"\n1.  Admin"
                    +"\n2.  Pembeli"
                    +"\n")
                role = input("Akun tersebut memiliki role apa? (1/2): ")

                if not role.isdigit() or role not in ['1', '2']:
                    os.system('cls')
                    print("Input role harus berupa angka 1 atau 2!!")
                    continue
                else:
                    break
        
        return addAccount(username, password, role)


# Kode untuk mengenkripsi dan memverifikasi password
daftar_huruf = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def enkripsi_password(password):
    kumpulan_enkripsi = []
    for i in password:
        kumpulan_enkripsi.append(chr(ord(i) + 4))
    
    karakter_acak = ""
    for karakter in kumpulan_enkripsi:
        karakter_acak += karakter
        karakter_acak += random.choice(daftar_huruf)

    return karakter_acak


def verifikasi_password(password_enkripsi, password):
    ambil_pw = password_enkripsi[::2]

    hasil_dekripsi = ""
    for i in ambil_pw:
        hasil_dekripsi += chr(ord(i) - 4)
    
    return True if hasil_dekripsi == password else False

# Kode fungsi untuk mengubah role ke teks
def role_parse(role):
    if role == 0:
        return 'Pemilik Toko'
    elif role == 1:
        return 'Admin'
    elif role == 2:
        return 'Pembeli'