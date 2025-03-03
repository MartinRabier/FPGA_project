import serial
import time



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
                self.ser = ser
            return ser
        except serial.SerialException as e:
            print("Erreur lors de l'ouverture du port :", e)
            return None
        
        
    def set_memory_addr(self,addr):
        commande = f"A{addr}"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                print(f"Réponse reçue: {reponse}")
            else:
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            print("Erreur lors de la lecture :", e)
            return None
    
    def write_val_mem(self,val):
        commande = f"W{val}"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                print(f"Réponse reçue: {reponse}")
            else:
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            print("Erreur lors de la lecture :", e)
            return None
        
    def display_mem_vals_leds(self):
        commande = "G"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            if reponse:
                reponse = reponse.decode('utf-8').strip()
                print(f"Réponse reçue: {reponse}")
            else:
                print("Aucune réponse reçue.")
            return reponse
        except Exception as e:
            print("Erreur lors de la lecture :", e)
            return None
            
    def read_mem_val(self) :
        commande = "R"
        if isinstance(commande, str):
            commande = commande.encode('utf-8')
        try:
            self.ser.write(commande)
            print(f"Commande envoyée: {commande}")
        except Exception as e:
            print("Erreur lors de l'envoi de la commande :", e)
            
        time.sleep(2)
        try:
            reponse = self.ser.read(self.ser.in_waiting or 1)
            symb = str(reponse)
            if reponse:
                print("Réponse reçue: ",symb[6:10])
            else:
                print("Aucune réponse reçue.")
            return symb[6:8]
        except Exception as e:
            print("Erreur lors de la lecture :", e)
            return None
            
    def close_instrument(self) :
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                print(f"Port {self.port} fermé avec succès.")
            else:
                print("Le port est déjà fermé ou non initialisé.")
        except Exception as e:
            print("Erreur lors de la fermeture du port :", e)
        


if __name__ == '__main__' :
    fpga = FPGA("COM10",115200,timeout=None)
    fpga.open_instrument()
    fpga.set_memory_addr("00")
    fpga.write_val_mem("FF")
    fpga.display_mem_vals_leds()
    mem_val = fpga.read_mem_val()
    print("Valeur lue :",mem_val)
    fpga.close_instrument()
    

