import socket

def send_file(file_path, ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        with open(file_path, 'rb') as f:
            s.sendall(f.read())
    print(f"File {file_path} sent")
