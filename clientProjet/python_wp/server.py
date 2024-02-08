import socket
import threading
import struct
import time

host, port = ('', 4443)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("C'est bon")
s.listen(5)

def recevoir_requete(client_socket):
        data = client_socket.recv(1024)
        version, typeEchange, typeMessage, Erreur, message = struct.unpack('HHHH100s', data)
        data = data.rstrip(b'\x00')
        print(data)
        print(f"Version : {version}")
        print(f"Type d'échange : {typeEchange}")
        print(f"Type de message : {typeMessage}")
        print(f"Erreur : {Erreur}")
        print(f"Message : {message.decode('utf-8')}") 
        response = f"Message reçu côté serveur : {version}, {typeEchange}, {Erreur}, {message.decode('utf-8')}"
        response = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, message)
        client_socket.sendall(response)
        
def envoyerRequeteConnexionPositive(client_socket):
        version = 1
        typeEchange = 1
        typeMessage = 2
        Erreur = 0
        data = ""
        #response = f"Message reçu côté serveur : {version}, {typeEchange}, {Erreur}, {message.decode('utf-8')}"
        response = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        client_socket.sendall(response.encode("utf-8"))
        
def envoyerToken(client_socket):
        version = 1
        typeEchange = 3
        typeMessage = 0
        Erreur = 0
        data = ""
        #response = f"Message reçu côté serveur : {version}, {typeEchange}, {Erreur}, {message.decode('utf-8')}"
        response = struct.pack('HHHH100s', version, typeEchange, typeMessage, Erreur, data[:100].encode('utf-8'))
        client_socket.sendall(response.encode("utf-8"))
        
def connexion():
        conn, address = s.accept()
        return conn

conn = connexion()

while True: 
    recevoir_requete(conn) 
    #conn.sendall("test".encode())
    #time.sleep(2)
    #envoyerToken

s.close()