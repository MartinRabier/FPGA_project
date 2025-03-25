import serial
import time
import logging
import collections
import threading
import os

#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class FPGA:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def read_single_0(self,path,line):
        file = open(path, 'r')
        
        try:
            self.send_parameter("W", line)
            #self.send_go_command() position 2
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier CSV: {e}")

        #send go
        time.sleep(1)
        self.send_go_command()
        time.sleep(1)
        response = self.ser.read(self.ser.in_waiting or 1)
        if response:
            ans = response.hex().upper()
            logging.info(f"Réponse reçue: {ans}")
        else:
            logging.info("Aucune réponse reçue.")
        encoded = bytes.fromhex(format(ord('T') + 1, '02X'))
        

        #get cipher
        encoded = bytes.fromhex(format(ord('C') + 1, '02X'))
        try:
            self.ser.write(encoded)
            logging.info(f"Commande envoyée (C): {encoded.hex().upper()}")
        except Exception as e :
            logging.error(f"Erreur lors de l'envoi de la commande C: {e}")
        time.sleep(0.5)
        response = self.ser.read(self.ser.in_waiting or 1)
        output = open("cipher.csv","wb")
        output.write(response.hex().upper())
        output.flush()
        output.close()
        if response:
            ans = response.hex().upper()
            logging.info(f"Réponse reçue: {ans}")
        else:
            logging.info("Aucune réponse reçue.")

        #get tag
        encoded = bytes.fromhex(format(ord('T') + 1, '02X'))
        try:
            self.ser.write(encoded)
            logging.info(f"Commande envoyée (T): {encoded.hex().upper()}")
        except Exception as e :
            logging.error(f"Erreur lors de l'envoi de la commande T: {e}")
        time.sleep(0.5)
        response = self.ser.read(self.ser.in_waiting or 1)
        if response:
            ans = response.hex().upper()
            logging.info(f"Réponse reçue: {ans}")
        else:
            logging.info("Aucune réponse reçue.")
    
    def read_data_0(self,path):
        file = open(path, 'r')
        lines = file.readlines()
        for line in lines:
            self.read_single_0(path,line)
        file.close()

    def open_instrument(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            if self.ser.is_open:
                logging.info(f"Port {self.port} ouvert avec succès.")
            return self.ser
        except serial.SerialException as e:
            logging.error(f"Erreur lors de l'ouverture du port {self.port}: {e}")
            return None

    def send_parameter(self, prefix, param, padding=""):
        if prefix == 'W' or 'w':
            padding = "800000"

        next_prefix = format(ord(prefix) + 1, '02X')
        param_bytes = bytes.fromhex(param)
        padding_bytes = bytes.fromhex(padding) if padding else b""
        msg = bytes.fromhex(next_prefix) + param_bytes + padding_bytes

        try:
            self.ser.write(msg)
            logging.info(f"Commande envoyée ({prefix}): {msg.hex().upper()}")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de la commande {prefix}: {e}")
        time.sleep(0.5)
        response = self.ser.read(self.ser.in_waiting or 1)
        if response:
            logging.info(f"Réponse reçue: {response}")
        else:
            logging.info("Aucune réponse reçue.")
        return response

    def read_cipher(self):
        
        encoded = bytes.fromhex(format(ord('C') + 1, '02X'))
        try:
            self.ser.write(encoded)
            logging.info(f"Commande envoyée (C): {encoded.hex().upper()}")
        except Exception as e :
            logging.error(f"Erreur lors de l'envoi de la commande C: {e}")
        time.sleep(0.5)
        response = self.ser.read(self.ser.in_waiting or 1)
        if response:
            ans = response.hex().upper()
            logging.info(f"Réponse reçue: {ans}")
        else:
            logging.info("Aucune réponse reçue.")
        

    def read_tag(self):
        
        encoded = bytes.fromhex(format(ord('T') + 1, '02X'))
        try:
            self.ser.write(encoded)
            logging.info(f"Commande envoyée (T): {encoded.hex().upper()}")
        except Exception as e :
            logging.error(f"Erreur lors de l'envoi de la commande T: {e}")
        time.sleep(0.5)
        response = self.ser.read(self.ser.in_waiting or 1)
        if response:
            ans = response.hex().upper()
            logging.info(f"Réponse reçue: {ans}")
        else:
            logging.info("Aucune réponse reçue.")
        

    def send_go_command(self):
        cmd = 'H' # Commande "Go"
        try:
            self.ser.write(cmd.encode('utf-8'))
            logging.info(f"Commande envoyée (Go): {cmd}")
        except Exception as e:
            logging.error("Erreur lors de l'envoi de la commande Go: " + str(e))
        



    def read_response(self):
        """
        Reads available response bytes from the FPGA.
        """
        time.sleep(0.5)
        try:
            response = self.ser.read(self.ser.in_waiting or 1)
        except serial.SerialTimeoutException:
            logging.error("Timeout lors de la lecture de la réponse.")
            return b""  # Retourner une chaîne vide en cas de timeout
        logging.info(f"Lecture réponse: {response.hex().upper()}")
        return response

    def close_instrument(self):
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                logging.info("Port fermé avec succès.")
            else:
                logging.info("Port déjà fermé.")
        except Exception as e:
            logging.error("Erreur lors de la fermeture du port: " + str(e))


# Live plotter for ECG waveform using matplotlib animation.
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



# --------------------------------------------------------------------
if __name__ == '__main__':
    # Example encryption parameters (hex strings without spaces)
    key = "8A55114D1CB6A9A2BE263D4D7AECAAFF"         # 16 bytes = 32 hex characters
    nonce = "4ED0EC0B98C529B7C8CDDF37BCD0284A"         # 16 bytes
    associated_data = "4120746F2042"               # 8 bytes
    ad_padding = "8000"                               # padding for associated data

    # Instantiate and open the FPGA instrument
    fpga = FPGA("COM9", 115200, timeout=1)
    fpga.close_instrument()
    fpga.open_instrument()

    # Send encryption parameters via UART
    fpga.send_parameter("K", key)                           # Key
    fpga.send_parameter("N", nonce)                         # Nonce
    fpga.send_parameter("A", associated_data, ad_padding)   # Associated Data with padding ("80 00")
    '''
    fpga.send_parameter("W", line)
    encoded = bytes.fromhex(format(ord('C') + 1, '02X'))
    fpga.ser.write(encoded)
    encoded = bytes.fromhex(format(ord('T') + 1, '02X'))
    fpga.ser.write(encoded)
    '''

    #fpga.read_data("waveform_example_ecg.csv")
    #fpga.read_single("waveform_example_ecg.csv")
    fpga.read_data_0("waveform_example_ecg.csv")
    

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
    # Keep the main thread alive for demonstration
    time.sleep(30)
    fpga.close_instrument()