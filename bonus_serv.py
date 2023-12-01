import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))

s.listen(1)


def unbinaire(msg):
    return int.from_bytes(msg, byteorder='big')


def binaire(msg):
    return msg.to_bytes((msg.bit_length() + 7) // 8, byteorder='big')


def send(result):
    header = len(binaire(result)).to_bytes(2, byteorder='big')
    seq_fin = "<clafin>".encode()
    return header + binaire(result) + seq_fin


def receive(conn):

    data = conn.recv(1)
    if data == b"":
        return
    print(f"Reçu {len(data)} octets")
    print(f"Reçu: {data}")
    msg_len = int.from_bytes(data[0:2], byteorder='big')

    print(f"Lecture des {msg_len} prochains octets")

    # Une liste qui va contenir les données reçues
    chunks = []

    bytes_received = 0
    while bytes_received < msg_len:
        # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
        chunk = conn.recv(min(msg_len - bytes_received,
                              1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')

        # on ajoute le morceau de 1024 ou moins à notre liste
        chunks.append(chunk)

        # on ajoute la quantité d'octets reçus au compteur
        bytes_received += len(chunk)
    fin = conn.recv(8)
    if fin.decode() != "<clafin>":
        raise RuntimeError('Invalid chunk received bro')
    else:
        # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message

        return b"".join(chunks)


def client_connection():
    conn, addr = s.accept()
    try:
        # On reçoit le calcul du client
        message_received = receive(conn)
        if message_received is None:
            conn.close()
            return
        first_header = int.from_bytes(message_received[0:2], byteorder='big')
        first_int = unbinaire(message_received[2: 2 + first_header])
        old = 2 + first_header
        signe = message_received[old:old + 1].decode()
        old += 1
        second_int = unbinaire(message_received[old:])
        res = eval(str(first_int) + signe + str(second_int))
        conn.send(send(res))

    except socket.error:
        print("Error Occured.")
    finally:
        conn.close()


while True:
    try:
        client_connection()
    except KeyboardInterrupt:
        print("Server stopped by user.")
        break
s.close()
