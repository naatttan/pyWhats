import socket
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
    
    
    # fonction ecoutant sur un socket et ressortant un dictionnaire contenant les différents champs du message
    def ecouter(self, sock: socket.socket):
        data = sock.recv(1024)
        strRcv = "{}".format(data.decode('utf-8'))
        # strRcv = data.decode()
        if self.server.DEBUG:
            print(f"[Recu] -> {data}")
        msgRcv = {
        'version': strRcv.split('//')[0],
        'typeEchange': strRcv.split('//')[1],
        'typeMessage': strRcv.split('//')[2],
        'erreur': strRcv.split('//')[3],
        'data': strRcv.split('//')[4]
        }
        if self.server.DEBUG:
            print(f"[Recu data] -> {msgRcv['data']}")
        return msgRcv
    
    # fonction envoyant la réponse pour une connexion
    def reponseConnexion(self, socket: socket.socket, numErreur: int, infoErreur: str):
        envoie = self.version + "//1//12//" + str(numErreur) + "//" + infoErreur
        socket.send(envoie.encode())
    
    # fonction envoyant la réponse pour la reception d'un message
    def reponseMessage(self, socket: socket.socket, numErreur: int, infoErreur: str):
        envoie = self.version + "//2//12//" + str(numErreur) + "//" + infoErreur
        socket.send(envoie.encode())
    
    # fonction envoyant le token d'envoie de fichier au client
    def envoieTokenFichier(self, socket: socket.socket):             
        envoie = self.version + "//3//10//0//"
        socket.send(envoie.encode())
    
    
    def reponseMessage(self, socket: socket.socket, numErreur: int, infoErreur: str):
        envoie = self.version + "//3//12//" + str(numErreur) + "//" + infoErreur
        socket.send(envoie.encode())
        

    
    def envoieMessageSynchro(self, socket: socket.socket, msg):
        data = str(msg.conv) + "\\" + msg.user + "\\" + str(msg.timer) + "\\" + msg.texte
        envoie = self.version + "//5//12//" + '0' + "//" + data
        socket.send(envoie.encode())
        pass
    
    def envoieListeMessageSynchro(self, socket: socket.socket, conv):
        pass
    
    def envoieFichier(self, socket: socket.socket, filePath: str):
        pass
    
    