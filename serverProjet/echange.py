import socket
import struct
# from conversation import Conversation, Message
# from session import Session
# from server import Server

class Echange:
    
    def __init__(self, adresse: str, port: int, server):
        self.addrServ = (adresse, port)
        self.sockServ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockServ.bind(self.addrServ)
        self.version = '1'
        self.server = server
        self.server.socket = self.sockServ
        
    def attendreConnexion(self):
        self.sockServ.listen()

    def acceptConnexion(self):
        return self.sockServ.accept()
    
    def fermerSocketServer(self):
        self.sockServ.close()
    
    
    # fonction ecoutant sur un socket et ressortant un dictionnaire contenant les différents champs du message
    def ecouter(self, sock: socket.socket):
        try:
            data = sock.recv(1024)
            # strRcv = "{}".format(data.decode('utf-8'))
            version, typeEchange, typeMessage, erreur, donnees = struct.unpack("IIII1008s", data)
            # strRcv = data.decode()
            
            # if self.server.DEBUG:
            #     print(f"[Recu] -> {data}")
            msgRcv = {
            'version': str(version),
            'typeEchange': str(typeEchange),
            'typeMessage': str(typeMessage),
            'erreur': str(erreur),
            'data': donnees.rstrip(b'\x00').decode()
            }
            if self.server.DEBUG:
                print(f"[Recu data] -> {msgRcv['data']}")
            return msgRcv
        except Exception as erreur:
            print(f"[Erreur ecoute] {erreur}")
    
    # fonction envoyant la réponse pour une connexion
    def reponseConnexion(self, socket: socket.socket, numErreur: int, infoErreur: str):
        # envoie = self.version + "//1//2//" + str(numErreur) + "//" + infoErreur
        envoie = struct.pack("IIII1008s", int(self.version), 1, 2, numErreur, infoErreur.encode())
        socket.send(envoie)
    
    # fonction envoyant la réponse pour la deconnexion
    def reponseDeconnexion(self, socket: socket.socket, numErreur: int, infoErreur: str):
        # envoie = self.version + "//1//3//" + str(numErreur) + "//" + infoErreur
        envoie = struct.pack("IIII1008s", int(self.version), 1, 3, numErreur, infoErreur.encode())
        socket.sendall(envoie)
    
    # fonction envoyant la réponse pour la reception d'un message
    def reponseMessage(self, socket: socket.socket, numErreur: int, infoErreur: str):
        # envoie = self.version + "//2//2//" + str(numErreur) + "//" + infoErreur
        envoie = struct.pack("IIII1008s", int(self.version), 2, 2, numErreur, infoErreur.encode())
        socket.send(envoie)
    
    # fonction envoyant le token d'envoie de fichier au client
    def envoieTokenFichier(self, socket: socket.socket):             
        envoie = self.version + "//3//0//0//"
        socket.send(envoie.encode())
        
    
    def envoieMessageSynchro(self, socket: socket.socket, msg):
        data = str(msg.conv) + "\\" + msg.user + "\\" + str(msg.timer) + "\\" + msg.texte
        # envoie = self.version + "//5//2//" + '0' + "//" + data
        envoie = struct.pack("IIII1008s", int(self.version), 5, 2, 0, data.encode())
        socket.send(envoie)
    
    def envoieListeMessageSynchro(self, socket: socket.socket, conv):
        pass
    
    def telechargementFichier(self, socket: socket.socket, filePath: str):
        with open(filePath, 'rb') as fichier_entree:
            donnees = fichier_entree.read(1004)
            while donnees:
                # modification de la structure pour ajouter la taille des données envoyées
                envoie = struct.pack("IIIII1004s", int(self.version), 4, 0, 0, len(donnees), donnees)
                socket.send(envoie)
                donnees = fichier_entree.read(1024)
    
    def telechargementFichierOk(self, socket: socket.socket):
        envoie = struct.pack("IIII1008s", int(self.version), 4, 3, 0, "".encode())
        socket.send(envoie)
        
    def telechargementFichierErreur(self, socket: socket.socket, numErreur: int, infoErreur: str):
        envoie = struct.pack("IIII1008s", int(self.version), 4, 3, numErreur, infoErreur.encode())
        socket.send(envoie)
    