import serial
import time
import logging
import collections
import threading
import os
import csv
from ascon_pcsn import ascon_decrypt, ascon_encrypt,demo_print

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections

def decrypt_cipher(line,line2,key,nonce,ad):
    key_b = bytes.fromhex(key)
    nonce_b = bytes.fromhex(nonce)
    cipher = line[:362]
    tag = line2[:32]
    temp = cipher+tag
    to_use = bytes.fromhex(temp)
    cipher_b = bytes.fromhex(cipher)
    #tag_b = bytes.fromhex(tag)
    ad_b=bytes.fromhex(ad)
    print(key_b,nonce_b,ad_b,to_use)
    decrypted_cipher = ascon_decrypt(key_b,nonce_b,ad_b,to_use,"Ascon-128")
    cipher_hex = decrypted_cipher.hex().upper()
    demo_print([("key", key_b), 
                ("nonce", nonce_b), 
                ("plaintext", cipher_b), 
                ("ass.data", ad_b), 
                ("ciphertext", decrypted_cipher[:-16]), 
                ("tag", decrypted_cipher[-16:]),  
               ])
    decrypted =[cipher_hex[:-32]]
    with open("decrypted_cipher.csv",mode='a',newline="") as output :
            writer = csv.writer(output)
            writer.writerow(decrypted)
    

def decrypt_file(path_cipher,path_tag,key,nonce,ad):
    ciphers = open(path_cipher,"r")
    tags = open(path_tag,"r")
    lines2 = tags.readlines()
    lines1 = ciphers.readlines()
    
    for line1,line2 in zip(lines1,lines2) : 
         decrypt_cipher(line1,line2,key,nonce,ad)
    ciphers.close()
    tags.close
     
def compare(path_wave,path_decrypted):
     waves = open(path_wave,"r")
     decrypted = open(path_decrypted,"r")
     lines1 = waves.readlines()
     lines2 = decrypted.readlines()
     lenght = len(lines1)
     cpt=0
     for line1,line2 in zip(lines1,lines2):
        print(type(line1),type(line2))
        print(line1,line2)
        if line1==line2 : 
            print("matching format")
            cpt+=1
        elif cpt==lenght-1:
            print("Files read")
     waves.close()
     decrypted.close()
     if cpt==lenght-1 :
         print("All waves are matching")
         return True
     else :
         print("Some waves aren't matching")
         return False
     


def plot_ECG(path):
    waves = open(path, "r")
    lines = waves.readlines()
    concatenate = ""

    for line in lines:
        concatenate += line.strip()
    try:
        decrypted_bytes = bytes.fromhex(concatenate)
        amplitudes = list(decrypted_bytes)
    except ValueError as e:
        print(f"Erreur de conversion hex -> int : {e}")
        return

    max_len = 200
    data = collections.deque([0] * max_len, maxlen=max_len)

    fig, ax = plt.subplots()
    line, = ax.plot(list(data))
    ax.set_ylim(-20, 300)  
    ax.set_title("ECG en temps réel")

    def update(frame):
        if frame < len(amplitudes):
            data.append(amplitudes[frame]) 
            line.set_ydata(list(data))
        return line,


    ani = animation.FuncAnimation(fig, update, frames=len(amplitudes), interval=50, blit=True, cache_frame_data=False)

    plt.show()


if __name__ == '__main__' :
    key = "8A55114D1CB6A9A2BE263D4D7AECAAFF"         
    nonce = "4ED0EC0B98C529B7C8CDDF37BCD0284A"         
    associated_data = "4120746F2042"               
    ad_padding = "8000"
    print(len(key),len(nonce))

    #decrypt_file("cipher.csv","tag.csv",key,nonce,associated_data)
    test=compare('waveform_parsed.csv','decrypted_cipher.csv')
    plot_ECG('decrypted_cipher.csv')
    


    