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
                self.users[username] = password # adds the current username and password set into the dictionary
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
                msg = userSocket.recv(1024)
                command = msg.split()[0] # the users command is the first word in the msg string

                if command == 'login':
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
            userSocket.send("There is already another user logged in")
            return
        username, password = msg.split()
        if username in self.users and self.users[username] == password:
            self.activeUser = username
            userSocket.send(username + "has logged in")
        else:
            userSocket.send("Username or password was incorrect")

    def newUser(self, userSocket, msg):
        if self.activeUser:
            userSocket.send("There is already another user logged in")
            return
        username, password = msg.split()
        if username in self.users:
            userSocket.send("That username is already in use")
        else:
            self.users[username] = password
            file = open('users.txt')
            file.write(username + ',' + password)
            userSocket.send("An account for" + username + "has been created")

    def sendMsg(self, userSocket, msg):
        if not self.activeUser:
            userSocket.send("You must be logged in to send messages")
            return

        outgoingMsg = ''.join(msg.split()[1:]) # removes the send command from the message
        userSocket.send(self.activeUser + ": " + outgoingMsg)

    def logout(self, userSocket, msg):
        if self.activeUser:
            self.activeUser = None
            userSocket.send("You have been logged out")
        else:
            userSocket.send("You are not logged in")

# Main, starting up the server with my port number
port = 14836
server = Server(port)
for username, password in server.users.items():
    print(f"Username: {username}, Password: {password}")
server.startServer()