import socket
import os
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 500 #4KB

def send_file(host, port):
    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host, port))
    print("Connected.\n")

    while(True):
        print(' 1) Download\n 2) Upload\n 3) Files next to the server\n 4) Exit')
        choose = input()
        if (choose == '1'):
            s.send('1'.encode())
            print('Please enter file name to download : ')
            filename = input()
            s.send(filename.encode())
            while(True):
                try:
                    received = s.recv(BUFFER_SIZE).decode()
                    if received =='not found':
                        print("Your entered file name not found. Please try again...")
                        break
                    filename, filesize = received.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filesize = int(filesize)
                    with open(filename, "wb") as f:
                        while True:
                            bytes_read = s.recv(BUFFER_SIZE)
                            if not bytes_read:    
                                continue
                            f.write(bytes_read)
                            break
                            
                    print("One file successfully recieved.\n")
                    break
                except:
                    break
        if (choose == '2'):
            s.send("2".encode())
            print('Please enter your file name')
            filename = input() 
            try:
                filesize = os.path.getsize(filename)
            except:
                print("File Not Found. Please try again...\n")
                continue
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            open(filename, "rb")
            
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break


                    s.sendall(bytes_read)

            print("One file successfully uploaded.\n")
        if (choose=='3'):
            s.send("3".encode())
            while(True):
                dir = s.recv(BUFFER_SIZE).decode()
                if dir != "":
                    print(dir)
                    break;
        if (choose=='4'):
            s.send("4".encode())
            s.close()
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    host = args.host
    port = args.port
    send_file(host, port)