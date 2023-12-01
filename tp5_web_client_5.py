import os
import socket


def unbinaire(msg: bytes) -> int:
    return int.from_bytes(msg, byteorder='big')


def check_http(msg: bytes) -> bool:
    return msg.decode().__contains__("HTTP/1.0 200 OK")


def receive(skt):
    data = skt.recv(4)
    if data == b"":
        return
    http_len = int.from_bytes(data[0:4], byteorder='big')
    chunks = []
    bytes_received = 0
    while bytes_received < http_len:
        chunk = skt.recv(min(http_len - bytes_received,
                             1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')
        chunks.append(chunk)
        bytes_received += len(chunk)
    if not check_http(b"".join(chunks)):
        return [False, b"".join(chunks)]
    data = skt.recv(4)
    if data == b"":
        return
    msg_len = int.from_bytes(data[0:4], byteorder='big')
    bytes_received = 0
    chunks1 = []
    while bytes_received < msg_len:
        chunk = skt.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')
        chunks1.append(chunk)
        bytes_received += len(chunk)
    return [True, b"".join(chunks1)]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
file = "image.jpg"
s.send(f"GET /{file}".encode())

s_data = receive(s)
if s_data is not None:
    if s_data[0]:
        if os.path.isfile(file):
            i = 0
            while True:
                if not os.path.isfile(f"{file.split('.')[0]}_{i}.{file.split('.')[1]}"):
                    file = f"{file.split('.')[0]}_{i}.{file.split('.')[1]}"
                    break
                i += 1
        with open(file, "wb") as f:
            f.write(s_data[1])
    else:
        print(s_data[1].decode())
s.close()
