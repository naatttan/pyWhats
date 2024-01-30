import time
import socket
import threading


# with open('./test.txt', 'wb') as file:
#     # print(file)
#     text = 'holaquetal\n'
#     file.seek(0)
#     file.write(text.encode())

# print(str(time.time()))
    
  
################################################################################################################
################################################################################################################


serveur_host = '127.0.0.1'  # Adresse IP du serveur
serveur_port = 12345         # Port du serveur

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serveur_host, serveur_port))

message = ''
while message.lower() != 'exit':
    message = input('>')
    data = "1//1//00//0//" + message
    client_socket.sendall(data.encode('utf-8'))


    donnees = client_socket.recv(1024)
    donnees_decodees = donnees.decode('utf-8')
    print("Réponse du serveur :", donnees_decodees)

# Fermeture de la connexion
client_socket.close()
