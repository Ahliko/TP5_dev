import socket


def binaire(msg: int) -> bytes:
    return msg.to_bytes((msg.bit_length() + 7) // 8, byteorder='big')


def unbinaire(msg: bytes) -> int:
    return int.from_bytes(msg, byteorder='big')


def send(lst, signe):
    header_int = len(binaire(lst[0])).to_bytes(2, byteorder='big')
    header = len(header_int + binaire(lst[0]) + signe.encode() + binaire(lst[1])).to_bytes(2, byteorder='big')
    seq_fin = "<clafin>".encode()
    return header + header_int + binaire(lst[0]) + signe.encode() + binaire(lst[1]) + seq_fin


def receive(skt):
    data = skt.recv(2)
    if data == b"":
        return
    msg_len = int.from_bytes(data[0:2], byteorder='big')
    chunks = []
    bytes_received = 0
    while bytes_received < msg_len:
        chunk = skt.recv(min(msg_len - bytes_received,
                                1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')
        chunks.append(chunk)
        bytes_received += len(chunk)
    fin = skt.recv(8)
    if fin.decode() != "<clafin>":
        raise RuntimeError('Invalid chunk received bro')
    else:
        return b"".join(chunks)


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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9999))

    s.send(send(lst, signe))

else:
    exit(1)

s_data = unbinaire(receive(s))
print(f"Résultat: {s_data}")
s.close()
