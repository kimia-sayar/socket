import socket
import os
import threading
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 1024 * 1000
SEPARATOR = "<SEPARATOR>"
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
dir = os.listdir()
def x(client_socket):
    while(True):
        choose = client_socket.recv(BUFFER_SIZE).decode()
        if (choose=='1'):
            while(True):
                filename = client_socket.recv(BUFFER_SIZE).decode()
                if filename in dir:
                    filesize = os.path.getsize(filename)
                    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
                    open(filename, "rb")
                    with open(filename, "rb") as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break

                            client_socket.sendall(bytes_read)
                    print("One file successfully uploaded.\n")
                    break
                else:
                    print("File Not Found.\n")
                    client_socket.send("not found".encode())
                    break
        if(choose=='2'):
            try:
                received = client_socket.recv(BUFFER_SIZE).decode()
                filename, filesize = received.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                with open(filename, "wb") as f:
                    while True:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:    
                            break
                        f.write(bytes_read)
                        break
                print("One file successfully recieved.\n")
            except:
                continue
        if (choose=='3'):  
            file_list = '\tLIST\n\n'
            for d in dir:
                file_list = file_list + '\t' +  d + "\n"
            client_socket.send(file_list.encode())
            print("file list sent.")
        if (choose=='4'): 
            client_socket.close() 
            print(f"[-] {address} is disconnected.")     
            break                   



if __name__ == "__main__": 
    while(True):
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        client_socket, address = s.accept()
        print(f"[+] {address} is connected.")
        t = threading.Thread(target=x, args=(client_socket,)) 
        t.start()