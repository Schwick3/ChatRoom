import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Command List: login (join the chatroom), newuser (format: newuser username password) (create a new account), send (send a message to the chatroom), logout (exit the chatroom)")
        except:
            print("Connection to the chatroom server failed")
            return

        receiver = threading.Thread(target=self.recMsg)
        receiver.start()
        self.sendMsg()

    def sendMsg(self):
        while True:
            msg = input()
            self.socket.send(msg.encode('utf-8'))

    def recMsg(self):
        while True:
            msg = self.socket.recv(1024).decode('utf-8')
            print(msg)

# Main, connecting to server and starting to receive and send messages

host = '127.0.0.1'
port = 14316
client = Client(host, port)
client.connect()
