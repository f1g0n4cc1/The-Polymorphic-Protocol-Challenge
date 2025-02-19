import socket
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

# Configurable traffic patterns
TRAFFIC_PATTERNS = {
    'normal': (1, 2),
    'burst': (0.1, 0.5),
    'slow': (5, 10)
}

# Novel encoding scheme
def novel_encode(data):
    return base64.b85encode(data.encode())

def send_message(mode, message):
    encoded_message = novel_encode(message)
    encrypted_message = cipher_suite.encrypt(encoded_message)
    return encrypted_message

def main():
    mode = random.choice(MODES)
    traffic_pattern = random.choice(list(TRAFFIC_PATTERNS.keys()))
    interval_range = TRAFFIC_PATTERNS[traffic_pattern]
    
    print(f'Initial mode: {mode}')
    print(f'Traffic pattern: {traffic_pattern}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            try:
                message = f'Hello from mode {mode}'
                encrypted_message = send_message(mode, message)
                s.sendall(encrypted_message)

                data = s.recv(1024)
                decrypted_data = cipher_suite.decrypt(data).decode()
                print(f'Received: {decrypted_data}')

                # Simulate mode blocking detection
                if random.random() < 0.1:
                    print(f'Mode {mode} blocked. Switching mode...')
                    mode = random.choice(MODES)
                    print(f'New mode: {mode}')

                time.sleep(random.uniform(*interval_range))

            except Exception as e:
                print(f'Error: {e}')
                break

if __name__ == "__main__":
    main()