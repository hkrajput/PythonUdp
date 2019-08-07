import socket   #for sockets
import sys  #for exit
import time
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = "localhost";
port = 8005;
while(1) :
    print host, port
    msg = raw_input('Enter message to send : ')
    try :
        start_time = time.time()
        for i in range(1,2):
            #Set the whole string
            print i
            s.sendto(str(i), (host, port))
            # receive data from client (data, addr)
            #d = s.recvfrom(1024)
            #reply = d[0]
            #addr = d[1]
            #print 'Server reply : nothing ', reply
        end_time = time.time()
        print "end Time++++++", end_time - start_time
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()



