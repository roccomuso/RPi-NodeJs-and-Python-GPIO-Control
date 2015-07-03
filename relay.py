import RPi.GPIO as GPIO  
import sys
import argparse
import inspect
import time
import BaseHTTPServer
import json

# Develpoed for python 2.7
# RPI command: nohup python relay.py -c listen 5000 &
# You can run this command on startup.

class rele:
    'Classe per pilotare un rele collegato al Raspberry Pi'
    
    state = "off"
    
    def __init__(self, PIN):
        if type(PIN) is int:
            self.pin = PIN
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin, GPIO.OUT)
        else:
            sys.exit('Pin deve essere di tipo intero - PIN '+PIN)

    def accendi(self):
        GPIO.output(self.pin,GPIO.HIGH)
        self.state = "on"

    def spegni(self):
        GPIO.output(self.pin,GPIO.LOW)
        self.state = "off"

    def blink(self, n, sec_attesa):
        sec_attesa = 2 if sec_attesa < 2 else sec_attesa
        # lampeggia n volte
        for i in range(n):
        
            GPIO.output(self.pin,GPIO.HIGH)
            time.sleep(sec_attesa)  
            GPIO.output(self.pin,GPIO.LOW)
            time.sleep(sec_attesa)

        self.state = "off"

    def toggle(self):
        if self.state == "off":
            self.accendi()
        else:
            self.spegni()
    
    def listen(self, porta):
        # permette di restare in ascolto di comandi esterni che commutino il rele
        porta = int(porta)
        if type(porta) is int and porta > 0 and porta < 65000:
            class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

                stopped = False
                
                def do_GET(s):

                    # analisi del s.path per estrapolare il comando e chiamare il metodo corretto...
                    percorso = s.path
                    cmd = percorso.split("/")
                    cmd = [x for x in cmd if x] # elimina componenti vuote.

                    # costrutto switch case, per l'esecuzione del comando
                    cmd_not_recognized = False

                    if len(cmd) > 0:
                        if cmd[0] == "accendi":
                            self.accendi()
                        elif cmd[0] == "spegni":
                            self.spegni()
                        elif cmd[0] == "toggle":
                            self.toggle()
                        elif cmd[0] == "blink":
                            n_vol = 3 if len(cmd) < 2 else int(cmd[1]) # se non specificato di default rimane 3
                            sec_att = 3 if len(cmd) < 3 else int(cmd[2]) # se non specificato di default rimane 3
                            self.blink(n_vol, sec_att)
                        else:
                            cmd_not_recognized = True
                    else:
                        cmd_not_recognized = True
       
                    if not cmd_not_recognized: # se comando riconosciuto, risposta con codice 200.
                        s.send_response(200)
                        s.send_header("Content-type", "application/json")
                        s.end_headers()
                        print('percorso richiesto: ', s.path)
                        s.wfile.write(json.dumps({'response_code': 200, 'new_state': self.state, 'path': s.path}))
                    else:
                        s.send_response(400)
                        s.send_header("Content-type", "application/json")
                        s.end_headers()
                        print('percorso richiesto: ', s.path)
                        s.wfile.write(json.dumps({'response_code': 400,'new_state': self.state, 'path': s.path}))

            httpd = BaseHTTPServer.HTTPServer(('', porta), RequestHandler)
            #httpd.socket.settimeout(10)
            #httpd.handle_request()
            httpd.serve_forever()
            print("server in ascolto...")
        else:
            sys.exit('La porta deve essere un valore intero compreso fra 0 e 65000 - '+porta)
        
        
    def termina(self):
        GPIO.cleanup()
        self.state = "off"


if __name__ == "__main__":

    # eseguito se chiamato singolarmente il file

    r = rele(11)

    parser = argparse.ArgumentParser(description="Accetta comandi e parametri per lanciarli da linea di comando")

    parser.add_argument('-c', '--comando', nargs="+", default=False, help="Definisci il comando da lanciare")

    args = parser.parse_args()
    #print(args)

    if len(sys.argv) > 1: # se vengono passati argomenti da linea di comando
        if (args.comando[0] != False and args.comando[0] != None):
            if hasattr(rele, args.comando[0]): # se esiste questo metodo nella classe rele

               for i in range(3): # rimuoviamo i 3 argomento: nome_script.py, -c, <comando>
                   sys.argv.pop(0)

               m = getattr(r, args.comando[0])
               if len(sys.argv) == (len(inspect.getargspec(m).args) -1): # argomenti che accetta il metodo
                   m(*sys.argv) # chiamiamo il metodo del rele istanziato e gli passiamo gli argomenti
               else:
                   sys.exit("Il metodo chiamato richiede un numero differente di argomenti")
               #print(sys.argv)
                      
           
            else:
                sys.exit('Non esiste un comando col nome fornito. I comandi equivalgono ai nomi dei metodi')
    

    else:
    
        while True:
            x = raw_input("inserisci comando: ")
            if x == 'accendi':
                r.accendi()
            elif x == 'spegni':
                r.spegni()
            elif x == 'blink':
                r.blink(int(raw_input('quante volte: ')), int(raw_input('secondi di intervallo: ')))
            elif x == 'toggle':
                r.toggle()
            elif x == 'ascolta':
                try:
                    r.listen(5000)
                except KeyboardInterrupt:
                    pass   
            elif x == 'stop':
                r.termina()
                break
        

    
