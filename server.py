import socket

# class for the server side
class Server:
    def __init__(self, port):
            self.IP = '127.0.0.1' # local host
            self.port = port # port with the last four of my student id
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # establishing the socket
            self.users = {} # dictionary of what users have accounts
            self.activeUser = None
            self.loadUsers()

    def loadUsers(self):
        try:
            file = open('users.txt')
            for line in file:
                username, password = line.strip().split(',') # removes whitespace in the current line and all commas
                self.users[username.strip()] = password.strip() # adds the current username and password set into the dictionary
        except:
            print("An error occured reading the users file")

    def startServer(self):
        self.socket.bind((self.IP, self.port))
        self.socket.listen(1)

        while True:
            userSocket, address = self.socket.accept()
            self.userConnection(userSocket)

    def userConnection(self, userSocket):
        while True:
            try:
                msg = userSocket.recv(1024).decode('utf-8')
                command = msg.split()[0].lower() # the users command is the first word in the msg string, makes it lowcase fo LOGIN, LoGiN, Login all work

                if command == 'login':
                    print(msg)
                    self.login(userSocket, msg)
                elif command == 'newuser':
                    self.newUser(userSocket, msg)
                elif command == 'send':
                    self.sendMsg(userSocket, msg)
                elif command == 'logout':
                    self.logout(userSocket, msg)

            except Exception as e:
                print("An error occured")


    def login(self, userSocket, msg):
        if self.activeUser:
            userSocket.send("There is already another user logged in".encode('utf-8'))
            return
        _, username, password = msg.split()
        print( username + ' ' + password)
        if username in self.users and self.users[username] == password:
            self.activeUser = username
            userSocket.send((username + " has logged in").encode('utf-8'))
        else:
            userSocket.send("Username or password was incorrect".encode('utf-8'))

    def newUser(self, userSocket, msg):
        if self.activeUser:
            userSocket.send("There is already another user logged in".encode('utf-8'))
            return
        _, username, password = msg.split()
        if username in self.users:
            userSocket.send("That username is already in use".encode('utf-8'))
        else:
            self.users[username] = password
            file = open('users.txt', 'a')
            file.write('\n' + username + ', ' + password)
            userSocket.send(("An account for " + username + " has been created").encode('utf-8'))
            file.close()

    def sendMsg(self, userSocket, msg):
        if not self.activeUser:
            userSocket.send("You must be logged in to send messages".encode('utf-8'))
            return

        msgParts = msg.split(maxsplit=1)

        command, outgoingMsg = msgParts
        userSocket.send((self.activeUser + ": " + outgoingMsg).encode('utf-8'))

    def logout(self, userSocket, msg):
        if self.activeUser:
            loogedOut = self.activeUser
            self.activeUser = None
            userSocket.send("You have been logged out".encode('utf-8'))
            userSocket.send((loogedOut + " has logged out").encode('utf-8'))
        else:
            userSocket.send("You are not logged in".encode('utf-8'))

# Main, starting up the server with my port number
port = 14316
server = Server(port)
for username, password in server.users.items():
    print(f"Username:{username} Password:{password}")
server.startServer()