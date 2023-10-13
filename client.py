import socket
import os
# share file function
def send_file(s, filename):
    if filename != 'q':
        s.send(('SEND ' + filename).encode())
        #if the file exist
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                bytes_to_send = f.read(1024)
                s.send(bytes_to_send)
                while bytes_to_send:
                    bytes_to_send = f.read(1024)
                    s.send(bytes_to_send)
        else:
            print("File does not exist!")
#this is the receive file function
def recv_file(s, filename):
    s.send(('FILE ' + filename).encode())
    data = s.recv(1024).decode()
    #if the space exist
    if data[:6] == 'EXISTS':
        filesize = int(data[7:])
        s.send(b'OK')
        with open('new_' + filename, 'wb') as f:
            data = s.recv(1024)
            total_recv = len(data)
            f.write(data)
            while total_recv < filesize:
                data = s.recv(1024)
                total_recv += len(data)
                f.write(data)
        print(f"{filename} has been received.")
    else:
        print("File does not exist on the server.")

def main():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket()
    s.connect((host, port))

    while True:
        message = input("-> ")
        if message == 'q':
            break
        elif message[:4] == 'FILE':
            filename = message[5:]
            recv_file(s, filename)
        elif message[:4] == 'SEND':
            filename = message[5:]
            send_file(s, filename)
        else:
            s.send(message.encode())
            data = s.recv(1024).decode()
            print(f"Received from server: {data}")

    s.close()

if __name__ == '__main__':
    main()
