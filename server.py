# ChatRoom Project Version One
# Skylar Perry
# Networks 1
# Fall 2024

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

    # opens and reads from the users.txt file
    def loadUsers(self):
        try:
            file = open('users.txt')
            for line in file:
                username, password = line.strip().split(',') # removes whitespace in the current line and all commas
                self.users[username.strip()] = password.strip() # adds the current username and password set into the dictionary
        except:
            print("An error occured reading the users.txt file")

    # starts the server and begins listening
    def startServer(self):
        self.socket.bind((self.IP, self.port))
        self.socket.listen(1)

        while True:
            userSocket, address = self.socket.accept()
            self.userConnection(userSocket)

    def userConnection(self, userSocket):
        # while loop that receives the messages
        while True:
            try:
                msg = userSocket.recv(1024).decode('utf-8')
                command = msg.split()[0].lower() # the users command is the first word in the msg string, makes it lowcase fo LOGIN, LoGiN, Login all work

                # uses the command to do what the user wants
                if command == 'login':
                    # print(msg)
                    self.login(userSocket, msg)
                elif command == 'newuser':
                    self.newUser(userSocket, msg)
                elif command == 'send':
                    self.sendMsg(userSocket, msg)
                elif command == 'logout':
                    self.logout(userSocket, msg)
                else:
                    userSocket.send(("Command " + command + " not found").encode('utf-8'))

            except Exception as e:
                print("An error occured connecting to the user")

    # checks if the credentials the user input are valid and logs them in
    def login(self, userSocket, msg):
        if self.activeUser:
            userSocket.send("There is already another user logged in".encode('utf-8'))
            return
        _, username, password = msg.split()
        # print( username + ' ' + password)
        if username in self.users and self.users[username] == password:
            self.activeUser = username
            print(username + " login")
            userSocket.send((username + " has logged in").encode('utf-8'))
        else:
            userSocket.send("Username or password was incorrect".encode('utf-8'))

    # creates a new user if there is not already a user with the username present. Also writes the new user to the users.txt file
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
            print("An account for " + username + " has been created")
            userSocket.send(("An account for " + username + " has been created").encode('utf-8'))
            file.close()

    # if the user is logged in sends a message to the chatroom
    def sendMsg(self, userSocket, msg):
        if not self.activeUser:
            userSocket.send("You must be logged in to send messages".encode('utf-8'))
            return

        msgParts = msg.split(maxsplit=1)

        command, outgoingMsg = msgParts
        outgoingMsg = (self.activeUser + ": " + outgoingMsg)
        print(outgoingMsg)
        userSocket.send(outgoingMsg.encode('utf-8'))

    # logs the user out and sends a message to the chatroom that they have logged out
    def logout(self, userSocket, msg):
        if self.activeUser:
            logedOut = self.activeUser
            self.activeUser = None
            print(logedOut + " logout")
            userSocket.send("You have been logged out".encode('utf-8'))
            userSocket.send((logedOut + " has logged out").encode('utf-8'))
        else:
            userSocket.send("You are not logged in".encode('utf-8'))

# Main, starting up the server with my port number
print("My chatroom server version one \n")
port = 14316
server = Server(port)
# for username, password in server.users.items():
#    print(f"Username:{username} Password:{password}")
server.startServer()