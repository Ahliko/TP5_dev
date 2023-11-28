import socket


def binaire(msg):
    return msg.to_bytes((msg.bit_length() + 7) // 8, byteorder='big')


msg = input("Calcul à envoyer: ")
msg = msg.replace(" ", "")
if msg.__contains__("+"):
    signe = "+"
elif msg.__contains__("-"):
    signe = "-"
elif msg.__contains__("*"):
    signe = "*"
else:
    print("Ce n'est pas un bon signe")
    exit(1)

if msg.__contains__(signe):
    msg_lst = msg.split(signe)
    lst = [0, 0]
    if len(msg_lst) != 2:
        print("Erreur de saisie")
        exit(1)
    try:
        lst[0] = int(msg_lst[0])
        lst[1] = int(msg_lst[1])
    except ValueError:
        print("Erreur de conversion")
        exit(1)
    for i in lst:
        if len(binaire(i)) > 4:
            print("Nombre trop grand")
            exit(1)
else:
    exit(1)

header = len(msg.encode()).to_bytes(4, byteorder='big')
print(len(msg.encode()))
seq_fin = "<clafin>".encode()
msg = header + msg.encode() + seq_fin
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

s.send(msg)

s_data = s.recv(1024)
print(s_data.decode())
s.close()
