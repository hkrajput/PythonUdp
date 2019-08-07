import asyncio
from multiprocessing import Pool, TimeoutError
import time
import os
from CalAmpParser import CalAmpParser
import binascii
global calamp
calamp = CalAmpParser()
import logging
#Create and configure logger 
logging.basicConfig(filename="server_log.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 



def send_to_parser(data):
    try:
        print ("start processing", data)
        global calamp
        calamp.start_process(data)
        #print ("end processing", data)
    except Exception as e:
        print (str(e))


class EchoServerProtocol:
    
    def main_worker(self, data):
        mp.apply_async(send_to_parser, (data,)) 
        print ("given data", data) 
        
    def connection_made(self, transport):
        self.transport = transport
    def get_ack(self, binary_data):
        binary_data = binary_data.decode('utf8')
        logger.debug(binary_data) 
        char_number = 0
        intial_char_count = 2
        mobile_id_length = int(binary_data[2:4], 16)
        #2 option byet , 2 mobile id length , mobile id length *2 + 4 sequemce number
        char_number += 4 + mobile_id_length*2 + 4
        ack = binary_data[:char_number] +"0201"
        ack = ack + binary_data[char_number + 4:char_number+8]
        #ack = ack +"0023"
        ack = ack + "020000000000"
        logger.debug("\n ack===||==" +str(ack)) 
        print ("ack=> ",ack)
        #return "83054864055902010102010000000000000000"

        return ack

    def datagram_received(self, data, addr):
        #print ("packet rec")
        #message = data.decode()
        binary_data = binascii.hexlify(data)
        print (binary_data, data)
        self.main_worker(binary_data)
        ack = self.get_ack(binary_data)
       # print (ack)
        ack = binascii.unhexlify(ack)
        print (ack,addr)
        self.transport.sendto(ack, addr)


if __name__ == '__main__':
    mp = Pool(processes=4)    
    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=('0.0.0.0', 8005))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

transport.close()
loop.close()
