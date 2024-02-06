import time
import socket
import threading
import queue
import os
import struct


# with open('./test.txt', 'wb') as file:
#     # print(file)
#     text = 'holaquetal\n'
#     file.seek(0)
#     file.write(text.encode())

# print(str(time.time()))
    
  
################################################################################################################
################################################################################################################

def reception():
    while not fermerThread:
        try:
            data = client_socket.recv(1024)
            # print(data)
            version, typeEchange, typeMessage, erreur, donnees = struct.unpack("IIII1008s", data)
            msg = (version, typeEchange, typeMessage, erreur, donnees)
            # print("--- " + donnees)
            # print(donnees.split("//")[1])
            try:
                if msg[1] == 5:
                    messages.put(msg)
                    
                    a = messages.get()
                    b = a[4].split("\\")
                    print(f"Message dans {b[0]}: {b[1]} - {b[3]} [{time.strftime('%H:%M:%S', time.gmtime(float(b[2])))}]")
                else:
                    reponses.put(msg)
            except Exception as erreur:
                print(f"[erreur insert stack] {erreur}")
        except socket.error as e:
            print(e)
            break

serveur_host = '127.0.0.1'  # Adresse IP du serveur
serveur_port = 12345         # Port du serveur

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((serveur_host, serveur_port))

fermerThread = False

messages =  queue.Queue() 
reponses = queue.Queue()

# echanges = ["1//1//0//0//kill\\kill",
#             "1//1//0//0//eva\\evalaplusbelle", 
#             "1//1//3//0//"]


echanges = [
    struct.pack("IIII1008s", 1, 1, 0, 0, "kill\\kill".encode()),
    struct.pack("IIII1008s", 1, 1, 0, 0, "eva\\evalaplusbelle".encode()),
    struct.pack("IIII1008s", 1, 1, 0, 0, "nathan\\mdp".encode()),
    struct.pack("IIII1008s", 1, 1, 0, 0, "non\\non".encode()),
    struct.pack("IIII1008s", 1, 1, 3, 0, "".encode()),
    struct.pack("IIII1008s", 1, 2, 0, 0, f"123\\eva\\{time.time()}\\voici mon message test !  ".encode()),
    struct.pack("IIII1008s", 1, 4, 1, 0, f"123\\eva\\test.pdf".encode())
]

####### Le fichier se transmet pas bien

def recevoirFichier():
    reponse = reponses.get()
    if not reponse[1] == 4: 
        print(f"reponse serveur: {reponse[4].decode().strip()}")
        return
    with open("./test.pdf", 'wb') as fichier_sortie:
        while reponse[2] == 0:
            # print(reponse)
            donnees_recues = reponse[4][4:][:struct.unpack('I', reponse[4][:4])[0]]
            # print(struct.unpack('I', reponse[4][:4])[0])
            fichier_sortie.write(donnees_recues)
            if reponses.empty() : break
            reponse = reponses.get()
    if reponse[2] == 3 and reponse[3] == 3:
        os.remove("./test.txt")
        print(f"reponse serveur: {reponse[4].decode().strip()}")
    # print(reponse)

ecouteur = threading.Thread(target=reception)
ecouteur.start()

inputUser = ''
while inputUser.lower() != 'exit':
    inputUser = input('>')
    client_socket.sendall(echanges[int(inputUser)])
    if inputUser == '6': recevoirFichier()
    try:
        if not reponses.empty():
            print("Réponse du serveur :", reponses.get()[4].decode().strip())
    except Exception as e:
        print(f"erreur: {e}")
        
client_socket.close()

fermerThread = True
ecouteur.join()



