import socket
import struct
import threading
# from cov import ChatInterface
from interface import Interface
import time
from PIL import Image
from io import BytesIO
import tkinter as tk

#host, port = ('localhost', 4443)

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#def envoyer_requete():
        #version = 1
        #data = input("Entrez un message (ou 'exit' pour quitter) : ")
        #pdu = struct.pack(f'I{len(data)}s', version, data.encode('utf-8'))
        #s.sendall(pdu)
        
class Client:
    def __init__(self):
        self.pseudonyme : str = 'evaLeSang'
        self.interface = Interface()
        self.conversations = {}
        #root = tk.Tk() 
        #self.interfaceApp = MessagerieApp(root) 
        self.host, self.port = ('localhost', 4443)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.connect((self.host, self.port))
            print("Client connecté")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            exit()
            
        #self.listen_thread = threading.Thread(target=self.ecouterMessages)
        #self.listen_thread.daemon = True  
        #self.listen_thread.start()
        
        #root.mainloop()
        
    def connexion(self):
        pseudonyme = input("Votre pseudo : ")
        password = input("Votre mot de passe : ")
        reponseServeur = self.recevoir_requete()
        version, typeEchange, typeMessage, Erreur, message = struct.unpack('HHHH1008s', reponseServeur)
        
        if typeEchange == 1 and typeMessage == 2 and Erreur == 0:
            self.pseudonyme = pseudonyme

    def afficher_informations(self):
        print(f"Nom: {self.pseudonyme}")
        
    def envoyermsg(self, message):
        #envoie msg sous forme de pdu
        #message = self.interfaceApp.envoyer_message()
        timer = 1  
        version = 1
        typeEchange = 2
        typeMessage = 0
        Erreur = 0
        conv = 1271
        data = str(conv) + "//" + self.pseudonyme + "//" + str(timer) + "//" + message
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        #pdu = struct.pack(f'I{len(texte)}s', version, typeEchange, texte.encode('utf-8'))
        self.s.sendall(pdu)
    
    def demanderToken(self):
        version = 1
        typeEchange = 3
        typeMessage = 1
        Erreur = 0
        conv = 1271
        data = str(conv) + "//" + self.pseudonyme 
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        self.s.sendall(pdu)
        reponseServeur = self.recevoir_requete()
        version, typeEchange, typeMessage, Erreur, message = struct.unpack('HHHH100s', reponseServeur)
        if typeEchange == 3 and typeMessage == 0 and Erreur == 0:
            self.demanderAlutilisateurFichier()
        
    def envoyerFichier(self, timer, message):   
        version = 1
        typeEchange = 3
        typeMessage = 0
        Erreur = 0
        conv = 1271
        data = str(conv) + "//" + self.pseudonyme + "//" + str(timer) + "//" + message
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        self.s.sendall(pdu)
        self.retourToken()

    def retourToken(self):
        version = 1
        typeEchange = 3
        typeMessage = 3
        Erreur = 0
        conv = 1271
        data = ""
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        self.s.sendall(pdu)
        
    def demanderAlutilisateurFichier(self):
        message = input("Entrez le chemin de votre fichier (ou 'exit' pour quitter) : ")
        timer = time()
        self.envoyerFichier(timer, message)
        
    #def demanderAlutilisateurMessage(self):
      #while True:
       # message = input("Entrez un message (ou 'exit' pour quitter) : ")
       # if message.lower() == 'exit':
         #   break
        #timer = time()
        #self.envoyermsg(timer, message)
        
    def demanderAlutilisateurTelechargement(self):
        message = input("Indiquez le nom du fichier (ou 'exit' pour quitter) : ")
        self.demanderTelechargement(message)
        
    def demanderTelechargement(self, message):
        version = 1
        typeEchange = 4
        typeMessage = 1
        Erreur = 0
        conv = 1271
        data = str(conv) + "//" + self.pseudonyme + "//" + message
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        self.s.sendall(pdu)
        if typeEchange == 4 and typeMessage == 2 and Erreur == 0:
            self.telechargerFichier(message)
    
    def telechargerFichier(self, message):
        with open(message, 'rb') as telechargementBinaire:
            contenu = telechargementBinaire.read(1008)
        image = Image.open(BytesIO(contenu))
        image.show()
        
    def demanderAlutilisateurCreationConv(self):
        nomConv = input("Indiquez le nom de votre conversation")
        users = input("Indiquez le ou les utilisateurs avec lesquels vous-voulez créer une conversation: ")
        self.creationConversation(nomConv, users)
        
    def creationConversation(self, nomConv, users):
        version = 1
        typeEchange = 6
        typeMessage = 0
        Erreur = 0
        data = nomConv + "//" + self.pseudonyme +  "//" + users
        pdu = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        self.s.sendall(pdu)
    
    def ecouterMessages(self):
        while True:
            message = self.recevoir_requete()
            self.interfaceApp.afficherMessage(message)
            
    def recevoir_requete(self):
        response = self.s.recv(1024).decode("utf-8")
        #print(response)
        return response
    
    def afficherConversations(self):
        for i in self.conversations.items():
            print (i)

    def run(self):
        #message = self.interface.apresConnexion
        #if message == 1:
            #self.demanderAlutilisateurCreationConv()
        #if message == 2:
            #self.afficherConversations()
            #message = self.interface.affichageConversations
        #if message == 3:
            #message = self.afficher_informations()
        
        message = self.interface.interieurConversation()
        if message == 1: 
            self.demanderAlutilisateurMessage()
        if message == 2: 
            self.demanderToken()
        if message == 3:
            self.demanderAlutilisateurTelechargement()
          
client = Client()
#client.run()

#while True:
    #client.envoyermsg()
    #client.demanderAlutilisateurMessage()
    #client.recevoir_requete()
    
