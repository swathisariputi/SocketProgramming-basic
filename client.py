#Name: Swathi Sariputi, Enrolment Number: BT19CSE098, Assignment-2

#Importing the neccesary libraries required
import socket
import sys

# get server details to connect.
host = sys.argv[1]
port = int(sys.argv[2])
# creating client socket
skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# try and except for terminating the connection
# connect client to server
try:
    skt.connect((host,port))
    # message to send to server
    print('Connected to server')
    msg = ""
    while True:
        msg=input("Please enter the message to the server : ")
        # send message to  server
        skt.send(msg.encode('ascii'))
        # receive message from server
        result = skt.recv(1024)
        # print the received message
        print('Received from the server :',str(result.decode('ascii')))
except ConnectionRefusedError :
    print("Error!!Connection failed-connection to server refused")
except KeyboardInterrupt:
    print("Closing client")

# close the connection
