import socket
import threading
import random
import time
from cryptography.fernet import Fernet
import base64

# Load the key from the key file
with open('key.key', 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Protocol modes
MODES = ['DNS', 'HTTPS', 'CustomUDP', 'Alternative', 'AsymmetricEncrypted', 'SymmetricEncrypted', 'InnovativeMode']

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    mode = random.choice(MODES)
    print(f'Initial mode: {mode}')

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            # Decrypt the received data
            decrypted_data = cipher_suite.decrypt(data).decode()
            print(f'Received (mode {mode}): {decrypted_data}')

            # Simulate mode blocking detection
            if random.random() < 0.1:
                print(f'Mode {mode} blocked. Switching mode...')
                mode = random.choice(MODES)
                print(f'New mode: {mode}')

            # Encrypt and send acknowledgment
            response = f'ACK from mode {mode}'.encode()
            encrypted_response = cipher_suite.encrypt(response)
            conn.sendall(encrypted_response)

        except Exception as e:
            print(f'Error: {e}')
            break

    conn.close()
    print(f'Disconnected by {addr}')

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()