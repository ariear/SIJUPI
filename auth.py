import csv as data
import os
from fungsi import enkripsi_password, verifikasi_password

path = os.getcwd()

# NOTES!!!
# Potensi error di signup jika input role selain angka
# signup bisa diisi spasi doang semua

def accountData():
    with open(path + '\\account.csv', mode='r') as file:
        reader = data.DictReader(file)
        dataAccount = list(reader)
    
    return dataAccount

def addAccount(username = None, password = None, role = None):
    password = enkripsi_password(password)
    if role is None:
        role = 2
    
    header = ['Username', 'Password', 'Role']
    with open(path + '\\account.csv', mode='a', newline='') as file:
        writer = data.DictWriter(file, fieldnames=header)
        writer.writerow({"Username":username, "Password":password, "Role":role})
    
    return "Akun Berhasil Dibuat!"

def login(errorMsg = False):
    os.system('cls')
    
    if errorMsg:
        print(errorMsg, "\n")
        
    print(f"{'LOGIN':^30}")
    
    while True:
        username = input("Masukkan Username anda: ")
        password = input("Masukkan Password anda: ")
        
        accounts = accountData()
        
        account = next((acc for acc in accounts if acc['Username'] == username), None)
            
        if account is None:
            return login("Maaf Username Atau Password Yang Anda Berikan Salah!")
        
        if not verifikasi_password(account["Password"], password):
            return login("Maaf Username Atau Password Yang Anda Berikan Salah!")
        
        break
    # print("Berhasil!")
    return [account["Username"], account["Role"]]
    
def signUp(errorMsg = False, superAdmin = False):
    os.system('cls')
    
    if errorMsg:
        print(errorMsg, "\n")
        
    print(f"{'REGISTRASI AKUN':^30}")
    
    while True:
        username = input("Masukkan Username anda (minimal 3 character!): ")
        password = input("Masukkan Password anda (minimal 8 character!): ")
        confirmedPassword = input("Konfirmasi Ulang Password anda: ")
        role = None
        
        if len(username) < 3:
            signUp("Username Akun Minimal 3 character!")
            return True
            
        accounts = accountData()
        account = next((acc for acc in accounts if acc['Username'] == username), None)
        
        if account is not None:
            signUp("Username Sudah Digunakan!")
            return True
        
        if len(password) < 8:
            signUp("Password Akun Minimal 8 character!")
            return True
        
        if password != confirmedPassword:
            signUp("Konfirmasi Ulang Password Berbeda Dengan Password Awal!")
            return True
        
        if superAdmin:
            print("\nROLE:"
                  +"\n1.Admin"
                  +"\n2.Konsumen"
                  +"\n")
            role = int(input("Akun tersebut memiliki role apa? (1/2): "))
        
        return addAccount(username, password, role)

# login()
# signUp()
# print(enkripsi_password("anjay123"))