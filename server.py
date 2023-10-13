import socket
import os
#simular send file function to client
def send_file(conn, filename):
    if os.path.exists(filename):
        conn.send(b'EXISTS ' + str(os.path.getsize(filename)).encode())
        user_response = conn.recv(1024).decode()
        if user_response[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytes_to_send = f.read(1024)
                conn.send(bytes_to_send)
                while bytes_to_send:
                    bytes_to_send = f.read(1024)
                    conn.send(bytes_to_send)
    else:
        conn.send(b'ERROR')

def recv_file(conn, filename):
    data = conn.recv(1024).decode()
    if data[:6] == 'EXISTS':
        filesize = int(data[7:])
        conn.send(b'OK')
        with open(filename, 'wb') as f:
            data = conn.recv(1024)
            total_recv = len(data)
            f.write(data)
            while total_recv < filesize:
                data = conn.recv(1024)
                total_recv += len(data)
                f.write(data)
    else:
        print("File does not exist!")

def main():
    #own ip address
    host = '127.0.0.1'
    #connect to own port number
    port = 12345

    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print("Server started. Waiting for connections...")
    conn, addr = s.accept()
    print(f"Connection from: {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data[:4] == 'FILE':
            filename = data[5:]
            recv_file(conn, filename)
        elif data[:4] == 'SEND':
            filename = data[5:]
            send_file(conn, filename)
        else:
            print(f"Received from client: {data}")
            message = input("-> ")
            conn.send(message.encode())

    conn.close()

if __name__ == '__main__':
    main()
