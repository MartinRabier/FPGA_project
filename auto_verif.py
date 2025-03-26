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
    decrypted =[cipher_hex]
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
     
    




class LiveECGPlot:
    def __init__(self, max_len=121):
        self.data = collections.deque([0] * max_len, maxlen=max_len)
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(list(self.data))
        self.ax.set_ylim(0, 255)
        self.ax.set_title("ECG Waveform")

    def update_plot(self, frame):
        self.line.set_ydata(list(self.data))
        return self.line,

    def start(self):
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=500, blit=True)
        plt.show()


if __name__ == '__main__' :
    key = "8A55114D1CB6A9A2BE263D4D7AECAAFF"         
    nonce = "4ED0EC0B98C529B7C8CDDF37BCD0284A"         
    associated_data = "4120746F2042"               
    ad_padding = "8000"
    print(len(key),len(nonce))

    decrypt_file("cipher.csv","tag.csv",key,nonce,associated_data)
    
    '''
    # Decrypt the ciphertext using the ASCON decryption function
    decrypted_hex = decrypt_ascon(key, nonce, associated_data + ad_padding, ciphertext_hex)
    logging.info(f"Decrypted hex: {decrypted_hex}")
    
    # Convert the decrypted hex string into decimal amplitude values (one value per byte)
    try:
        decrypted_bytes = bytes.fromhex(decrypted_hex)
        amplitudes = list(decrypted_bytes)
        logging.info(f"Amplitudes: {amplitudes}")
    except Exception as e:
        logging.error("Erreur lors de la conversion du hex décrypté en valeurs numériques: " + str(e))
        amplitudes = [0] * 121

    # Set up a live plot for the ECG waveform.
    plotter = LiveECGPlot(max_len=len(amplitudes))
    # Update the deque with the decrypted amplitudes.
    plotter.data = collections.deque(amplitudes, maxlen=len(amplitudes))
    # Start the live ECG plot in a separate thread (non-blocking)
    threading.Thread(target=plotter.start, daemon=True).start()
    '''