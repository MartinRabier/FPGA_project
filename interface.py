import serial
import time
import logging
from ascon_pcsn import demo_aead2
#test git

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.setLevel(logging.DEBUG)

class FPGA :
    def __init__(self,port,baud_rate,timeout):
        self.port = port
        self.baud_rate=baud_rate
        self.timeout = timeout
        self.ser = None
        
    def open_instrument(self):
        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            if ser.is_open:
                print(f"Port {self.port} ouvert avec succès.")
                logger.info(f"FPGA connecté sur le port {self.port}, baud rate =  {self.baud_rate}")
                self.ser = ser
            return ser
        except serial.SerialException as e:
            print("Erreur lors de l'ouverture du port :", e)
            logger.debug(f"Echec de la connexion du port {self.port}")
            return None
        
        
    def set_memory_addr(self,addr):
        commande = f"A{addr}"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            logger.info(f"Envoi de la commande : {commande}")
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            logger.warning(f"Echec de la sélection de l'adresse {commande}")
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                logger.debug(f"Commande {commande} reçue par le FPGA, réponse {reponse}")
                print(f"Réponse reçue: {reponse}")
            else:
                logger.debug(f"Aucune réponse de séléction d'adresse reçue")
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            logger.warning(f"Erreur de lecture de la réponse")
            print("Erreur lors de la lecture :", e)
            return None
    
    def write_val_mem(self,val):
        commande = f"W{val}"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            logger.info(f"Envoi de la commande : {commande}")
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            logger.warning(f"Echec de l'écriture de la valeur {val}")
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                logger.debug(f"Commande {commande} reçue par le FPGA, réponse {reponse}")
                print(f"Réponse reçue: {reponse}")
            else:
                logger.debug(f"Aucune réponse d'écriture reçue")
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            logger.warning(f"Erreur de lecture de la réponse")
            print("Erreur lors de la lecture :", e)
            return None
        
    def display_mem_vals_leds(self):
        commande = "G"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            logger.info(f"Envoi de la commande : {commande}")
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            logger.warning(f"Echec de l'envoie de la commande {commande}")
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                logger.debug(f"Commande {commande} reçue par le FPGA, réponse {reponse}")
                print(f"Réponse reçue: {reponse}")
            else:
                logger.debug(f"Aucune réponse de lecture reçue")
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            print("Erreur lors de la lecture :", e)
            logger.warning(f"Erreur de lecture de la réponse")
            return None
            
    def read_mem_val(self) :
        commande = "R"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            logger.info(f"Envoi de la commande : {commande}")
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            logger.warning(f"Echec de l'envoie de la commande {commande}")
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            symb = str(reponse)
            if reponse:
                logger.debug(f"Commande {commande} reçue par le FPGA, réponse {symb[6:10]}")
                print("Réponse reçue: ",symb[6:10])
            else:
                logger.debug(f"Aucune réponse de lecture reçue")
                print("Aucune réponse reçue.")
            return symb[6:8]
        except Exception as e:
            logger.warning(f"Erreur de lecture de la réponse")
            print("Erreur lors de la lecture :", e)
            return None
            
    def close_instrument(self) :
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                logger.info(f"fermeture du port {self.port}")
                print(f"Port {self.port} fermé avec succès.")
            else:
                logger.debug(f"Port {self.port} déjà fermé ou jamais initialisé")
                print("Le port est déjà fermé ou non initialisé.")
        except Exception as e:
            logger.debug(f"Echec de la fermeture du port {self.port}")
            print("Erreur lors de la fermeture du port :", e)
        


if __name__ == '__main__' :
    fpga = FPGA("COM3",115200,timeout=None)
    fpga.open_instrument()
    fpga.set_memory_addr("00")
    fpga.write_val_mem("FF")
    fpga.display_mem_vals_leds()
    mem_val = fpga.read_mem_val()
    print("Valeur lue :",mem_val)
    fpga.close_instrument()