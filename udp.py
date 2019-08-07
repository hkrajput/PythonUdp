import socket
import sys
import binascii
import struct
import time
import MySQLdb
db = MySQLdb.connect("localhost","root","root","eld_gps" )
cursor = db.cursor()

HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 8005 # Arbitrary non-privileged port

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

while 1:
    fl =open("data_gps.txt", "a")
    end = time.time()
    d = s.recvfrom(2048)
    data = d[0]
    addr = d[1]
    st = time.time()
    print binascii.hexlify(data)
    s.sendto(d[0], d[1])
    if len(binascii.hexlify(data))>=106:
        fl.write(binascii.hexlify(data))
        epoch = int(time.time())
        query = " INSERT INTO data_gps (`packet`, `entry_time`) values( '"+ binascii.hexlify(data) +"', '"+str(epoch)+"' );"
        print query
        cursor.execute(query)
        db.commit()
    fl.close()




    
   
