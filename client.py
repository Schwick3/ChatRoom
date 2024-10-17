# ChatRoom Project Version One
# Skylar Perry
# Networks 1
# Fall 2024
# This is the client side of the chatroom, it handles sending messages to the server and checks to make sure the commands are valid

import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connects to the server
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Command List: login (join the chatroom), newuser (format: newuser username password) (create a new account), send (send a message to the chatroom), logout (exit the chatroom)")
        except:
            print("Connection to the chatroom server failed")
            return

        # a lil multithreading so that we can send and receive messages at the same time
        receiver = threading.Thread(target=self.recMsg)
        receiver.start()
        self.sendMsg()

    # waits for user input then sends it to the server
    def sendMsg(self):
        while True:
            msg = input()
            # command variable to help validate commands
            command = msg.split()[0]
            if command == 'login':
                if len(msg.split()) < 3:
                    print("Not enough arguments to login. You have have username and password")
                    continue
            if command == 'newuser':
                msgParts = msg.split(maxsplit=2)
                # making sure the commands are being used correctly, if not skips them
                if len(msgParts) < 3:
                    print("Not enough arguments to create a new user. You have have username and password.")
                    continue
                _, username, password = msgParts
                if len(username) > 32 or len(username) < 3:
                    print("Username must be between 3 and 32 characters")
                    continue
                if len(password) > 8 or len(password) < 4:
                    print("Password must be between 4 and 8 characters")
                    continue
            if command == 'send':
                msgParts = msg.split(maxsplit=1)
                # making sure the commands are being used correctly, if not skips them
                if len(msg.split()) < 2:
                    print("Not enough arguments to send a message.")
                    continue
                _, outgoingMsg = msgParts
                if len(outgoingMsg) > 256 or len(outgoingMsg) == 0 or len(msgParts) < 2:
                    print("Message must be between 1 and 256 characters")
                    continue

            self.socket.send(msg.encode('utf-8'))

    # receives and prints the messages from the server
    def recMsg(self):
        while True:
            msg = self.socket.recv(1024).decode('utf-8')
            print(msg)

# Main, connecting to server and starting to receive and send messages
print("My chatroom client version one\n")

host = '127.0.0.1'
port = 14316
client = Client(host, port)
client.connect()
