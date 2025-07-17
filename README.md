# Diffie-Hellman-Algorithm

# Secure Chat Client with Diffie-Hellman Key Exchange

This is a Python-based secure chat client application that uses **Diffie-Hellman key exchange** to establish an encrypted session. It leverages **AES (CTR mode)** for message encryption and provides a simple **Tkinter GUI** for message input and display.

---

## 🔐 Features

- Two-phase **Diffie-Hellman key exchange** to derive a session key
- **AES encryption** (CTR mode) for secure message transmission
- Lightweight **GUI** using Tkinter
- XOR-based session key derivation for enhanced security

---

## 📦 Requirements

Install the following dependencies before running:

```bash
pip install pyaes



File Structure
Client: Main class that handles the TCP connection, key exchange, and message encryption.

Math: Utility module for generating Diffie-Hellman parameters (generate_generator_and_prime).

DiffieHellman: Class that handles key generation and shared secret calculation.

main: Launches the GUI and handles user input and interaction.





Ensure the server is running and listening on the specified host/port.

Run the client:
python client.py



Example Usage
Type a message in the entry field.

Press "Enter" or click the "Send" button.

Your message is encrypted and sent securely to the server.
To quit, type:
{quit}

 Dependencies
socket — For TCP client communication

pyaes — For AES-CTR encryption

tkinter — For GUI

Math (custom) — For prime and generator generation

DiffieHellman (custom) — For handling key exchange

📌 Notes
This is the client side. Ensure your server implementation matches the protocol and encryption method.

This example uses custom Diffie-Hellman and Math modules. You must include or implement Math.py and DiffieHellman.py accordingly.
