#Name: Swathi Sariputi, Enrolment Number: BT19CSE098, Assignment-2
#server1.py
#Importing the neccesary libraries required
import socket
import sys
import re
import logging

# for debug output set it to logging.DEBUG
logging.root.setLevel(logging.WARNING)

#  funtion to evaluate the given input string and return value
def calculator(inp):
    inp = inp.decode()  # decoding the given input
    reg_ex = r"^[0-9 -+/*(.)]+$"  # re that accepts only the mathematical expressions
    if bool(re.match(reg_ex , inp)):
        try:
            temp = str(eval(inp))
        except Exception as e:
            temp = str(e)
    else:
        temp = "invalid input"
    logging.debug("Server received : %s ", inp)
    logging.debug("Server Send     : %s ",temp)
    temp = temp.encode()
    return temp

def serve(cli, cli_addr):
    while True:
        # message received from client
        msg = cli.recv(1024)
        if not msg:
            print("  disconnected from ", cli_addr[1])
            break
        print('Client socket sent message: ',str(msg.decode('ascii')))
        res=calculator(msg)
        print('Sending reply: ',str(res.decode('ascii')))
        #send result to client
        cli.send(res)
    # connection closed
    cli.close()

# get server details
host = sys.argv[1]
port = int(sys.argv[2])
print("socket binded to port ", port)

try:
    # a infinite loop until client exit (ctrl+C)
    while True:
        # Creating a TCP/IP socket
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Binding the socket to the port
        skt.bind((host, port))
        # put the socket into listening mode
        skt.listen(5)
        #connect with client
        cli, cli_addr = skt.accept()
        # closing socket as soon as we get one request as this accepts only one client and to avoid multiple
        skt.close()
        print("Connected to :", cli_addr[0],":", cli_addr[1])
        serve(cli, cli_addr)
except KeyboardInterrupt:
    skt.close()
    print("Closing Server")


# close the server socket