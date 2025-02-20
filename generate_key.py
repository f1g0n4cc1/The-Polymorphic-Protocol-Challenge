from cryptography.fernet import Fernet

# Generate the encryption key
key = Fernet.generate_key()

# Save the key to a file
with open("key.key", "wb") as key_file:
    key_file.write(key)  # This line should be indented

print("Key generated and saved in key.key")