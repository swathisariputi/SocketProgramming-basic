#Name: Swathi Sariputi, Enrolment Number: BT19CSE098, Assignment-2
#server3.py
#Importing the neccesary libraries required
import socket
import sys
import logging
import queue
import select

# for debug output set it to logging.DEBUG
logging.root.setLevel(logging.WARNING)

# get server details
host = sys.argv[1]
port = int(sys.argv[2])
# Creating a TCP/IP socket
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.setblocking(0)
# Binding the socket to the port
skt.bind((host, port))
print("socket binded to port", port)
# put the socket into listening mode for incoming connections
skt.listen(5)
inputs = [skt]
# Sockets to which we expect to write
outputs = []
message_queues = {}

# Wait for at least one of the sockets to be ready for processing
try:
    while inputs:
        read, writ, excepts = select.select(inputs, outputs, inputs)
        for s in read: #"readable" socket
            if s is skt:
                # connect with client
                cli, cli_addr = s.accept()
                print("Connected to :", cli_addr[0], ":", cli_addr[1])
                cli.setblocking(0)
                inputs.append(cli)
                # Give the connection a queue for message we want to send
                message_queues[cli] = queue.Queue()
            else:
                # message received from client
                msg = s.recv(1024)
                if msg:
                    print('Client ',cli_addr,' socket sent message: ',str(msg.decode('ascii')))
                    # A readable client socket has message from client
                    logging.debug("Server received ({}) : {!r}  ".format(s.getpeername()[1], msg))
                    message_queues[s].put(msg)
                    # Add to output channel for response
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # Interpret empty result as closed connection
                    print("  disconnected from", s.getpeername()[1])
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writ:#writability.
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                # No messages waiting so stop checking for writability.
                outputs.remove(s)
            else:
                logging.debug("Server Send     (%s) : %s  ", s.getpeername()[1], next_msg)
                print('Sending reply: ',next_msg)
                #send echo to client
                s.send(next_msg)

        # Handle "exceptional conditions"
        for s in excepts:
            logging.warning("exception condition on %s", s.getpeername()[1])
            # Stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
except KeyboardInterrupt:
    skt.close()
    print("Server closing")

# close the server socket