import logging
import socket
import os

import colorlog

if not os.path.isfile("/var/log/web-server/bs_server.log"):
    os.makedirs("/var/log/web-server/", exist_ok=True)
    open("/var/log/web-server/bs_server.log", "w").close()

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/var/log/web-server/web_server.log', 'w', 'utf-8')
file_handler.setLevel(logging.INFO)
stream_handler = colorlog.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s %(levelname)s %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))

s.listen(1)


def header(msg):
    return len(msg).to_bytes(4, byteorder='big')


def client_connection():
    conn, addr = s.accept()
    try:
        # On reçoit le calcul du client
        data = conn.recv(1024)
        if not data:
            conn.close()
            return
        data = data.decode()
        if not (data.__contains__("GET /") and data.index("GET /") == 0):
            if data.__contains__("HTTP/1.1"):
                logger.warning(f"{addr[0]} {data.split('HTTP/1.1')[0]} 400 Bad Request HTTP/1.1")
            else:
                logger.warning(f"{addr[0]} {data} 400 Bad Request HTTP/1.1")
            envoie = "HTTP/1.1 400 Bad Request\n\n<html>\
                                <head><title>400 Bad Request</title></head>\
                                <body>\
                                <center><h1>400 Bad Request</h1></center>\
                                </body>\
                                </html>\
                                ".encode()
            conn.send(header(envoie) + envoie)
            conn.close()
            return
        if data[5] == " ":
            if data.__contains__("HTTP/1.1"):
                logger.warning(f"{addr[0]} {data.split('HTTP/1.1')[0]} 404 Not Found HTTP/1.1")
            else:
                logger.warning(f"{addr[0]} {data} 404 Not Found HTTP/1.1")
            envoie = "HTTP/1.1 404 Not Found\n\n<html>\
                                        <head><title>404 Not Found</title></head>\
                                        <body>\
                                        <center><h1>404 Not Found</h1></center>\
                                        </body>\
                                        </html>\
                                        ".encode()
            conn.send(header(envoie) + envoie)
            conn.close()
            return
        if not os.path.isfile(f"{data[5:].split(' ')[0]}"):
            if data.__contains__("HTTP/1.1"):
                logger.warning(f"{addr[0]} {data.split('HTTP/1.1')[0]} 404 Not Found HTTP/1.1")
            else:
                logger.warning(f"{addr[0]} {data} 404 Not Found HTTP/1.1")
            envoie = "HTTP/1.1 404 Not Found\n\n<html>\
                                            <head><title>404 Not Found</title></head>\
                                            <body>\
                                            <center><h1>404 Not Found</h1></center>\
                                            </body>\
                                            </html>\
                                            ".encode()
            conn.send(header(envoie) + envoie)
            conn.close()
            return
        with open(f"{data[5:].split(' ')[0]}", "rb") as f:
            if data.__contains__("HTTP/1.1"):
                logger.info(f"{addr[0]} {data.split('HTTP/1.1')[0]} 200 OK HTTP/1.1")
            else:
                logger.info(f"{addr[0]} {data} 200 OK HTTP/1.1")
            file = f.read()
            conn.sendall(
                header(f"HTTP/1.0 200 OK\n\n".encode()) + f"HTTP/1.0 200 OK\n\n".encode() + header(file) + file)
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
