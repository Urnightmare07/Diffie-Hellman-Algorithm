import socket
from Math import Math
from DiffieHellman import DiffieHellman
import pyaes
import tkinter

class Client:
    def __init__(self, host, port):
        destination = (host, port)
        self.__tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp_client.connect(destination)

    def establish_session(self):
        generator1, prime1 = Math.generate_generator_and_prime(256)
        self.__tcp_client.send(bytes(str(generator1), 'utf8'))
        self.__tcp_client.send(bytes(str(prime1), 'utf8'))
        
        diffie_hellman1 = DiffieHellman(generator1, prime1)
        result1 = diffie_hellman1.get_result()
        self.__tcp_client.send(bytes(str(result1), 'utf8'))
        
        result_from_server1 = int(self.__tcp_client.recv(1024))
        self.__key1 = diffie_hellman1.calculate_shared_secret(result_from_server1)

        generator2, prime2 = Math.generate_generator_and_prime(256)
        self.__tcp_client.send(bytes(str(generator2), 'utf8'))
        self.__tcp_client.send(bytes(str(prime2), 'utf8'))

        diffie_hellman2 = DiffieHellman(generator2, prime2)
        result2 = diffie_hellman2.get_result()
        self.__tcp_client.send(bytes(str(result2), 'utf8'))

        result_from_server2 = int(self.__tcp_client.recv(1024))
        self.__key2 = diffie_hellman2.calculate_shared_secret(result_from_server2)

        xorkey = self.__key1 ^ self.__key2
        newk1 = self.__key1 % xorkey
        newk2 = self.__key2 % xorkey
        self.__key = newk1 ^ newk2
        
        print("Session key: " + str(self.__key))

        self.__key = self.__key.to_bytes(32, byteorder="big")
        self.__aes = pyaes.AESModeOfOperationCTR(self.__key)

    def send_message(self, message):
        message = self.__aes.encrypt(message)
        print("Encrypted message: " + str(message))
        self.__tcp_client.send(message)

if __name__ == "__main__":
    def send(event=None):  # event is passed by binders.
        # Handles sending of messages
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        msg_list.insert("end", msg)
        client.send_message(msg)
        if msg == "{quit}":
            top.quit()

    def on_closing(event=None):
        # This function is to be called when the window is closed.
        my_msg.set("{quit}")
        send()

    top = tkinter.Tk()
    top.title("Chatter")

    messages_frame = tkinter.Frame(top)

    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")

    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()

    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    client = Client("localhost", 5000)
    client.establish_session()

    tkinter.mainloop()
