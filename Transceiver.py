import socket

"""
Tranceiver class is used to send and receiver UDP messages over the network using its send(),
and receive() functions. 
"""
class Transceiver:
    
#Default Constructor: Takes no arguments
    def __init__(self):
        self.senderIP     = ""
        self.receiverIP   = "127.0.0.1"
        self.senderPort   = ""
        self.receiverPort = 5005
        self.msg = ""
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.receiverIP, self.receiverPort)) 

#Receiver function receives data sent by the sender. Needs to be called inside an infinite loop
#before sending any packet
    def receive(self):
        data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        self.senderIP, self.senderPort = addr # Saves the SenderIP and senderPort for future use
        msg = data.decode("utf-8")            # Converts received bytes message to string
        return msg

#Sends data back to the sender
    def send(self, msg):
        byteMsg = bytes(self.msg, "UTF-8")
        self.sock.sendto(byteMsg, (self.senderIP, self.senderPort))


#Getter methods:
    def getSenderIP(self):
        return self.senderIP

    def getSenderPort(self):
        return self.senderPort

    def getReceiverIP(self):
        return self.receiverIP

    def getReceiverPort(self):
        return self.receiverPort


#Setter methods
    def setSenderIP(self, senderIP):
        self.senderIP = senderIP

    def setSenderPort(self, senderPort):
        self.senderPort = senderPort

    def setReceiverIP(self, receiverIP):
        self.receiverIP = receiverIP

    def setReceiverPort(self, receiverPort):
        self.receiverPort = receiverPort

#########################################END OF CLASS############################################
"""
tr = Transceiver()
print("Sent: Hello!") 
tr.send("Hello!")
tr.receive()
print("SenderIP: ", tr.getSenderIP())
"""
