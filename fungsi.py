import random

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
