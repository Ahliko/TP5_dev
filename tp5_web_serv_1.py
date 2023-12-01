import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))

s.listen(1)


def client_connection():
    conn, addr = s.accept()
    try:
        # On reçoit le calcul du client
        data = conn.recv(1024)
        if not data:
            conn.close()
            return
        data = data.decode()
        print(data)
        if not (data.__contains__("GET /") and data.index("GET /") == 0):
            conn.send("HTTP/1.1 400 Bad Request\n\n<html>\
                    <head><title>400 Bad Request</title></head>\
                    <body>\
                    <center><h1>400 Bad Request</h1></center>\
                    </body>\
                    </html>\
                    ".encode())
            conn.close()
            return
        conn.send("HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>".encode())
        conn.close()
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
