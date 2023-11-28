import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))

s.listen(1)
conn, addr = s.accept()

while True:
    try:
        # On reçoit le calcul du client
        data = conn.recv(4)
        if data == b"":
            break
        msg_len = int.from_bytes(data[0:4], byteorder='big')

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
            print("oui")
            # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
            message_received = b"".join(chunks)
            res = eval(message_received.decode())
            conn.send(str(res).encode())

    except socket.error:
        print("Error Occured.")
        break

conn.close()
