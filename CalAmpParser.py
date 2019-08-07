import binascii
from DbHandler import DbConnector
import time

class CalAmpParser():
    def __init__(self):
        self.conn =  DbConnector()

    def get_value_from_2compli(self, hex_string):
        # print hex_string
        dec = int(hex_string, 16)
        binary = bin(dec)
        real_binary = binary[2:]
        padding_len = 32 - len(real_binary)
        padding = ""
        for i in range(0, padding_len):
            padding += "0"
        real_binary = padding + real_binary
        sign_bit = real_binary[0]

        if sign_bit == "1":
            return (-1 * (int(''.join('1' if x == '0' else '0' for x in real_binary), 2) + 1))
        else:
            return int(real_binary, 2)


    def start_process(self, data):
        print ("processing start")
        #binary_data = binascii.hexlify(data)
        binary_data = data.decode('utf8')
        if not len(binary_data) >= 106:
            return False
        b = binary_data
        ack_msg = ""
        #print ("processing 2 2 2 start")
        try:
            parse_data = {
                "optional_bytes": b[0:2],
            }
            #ack_msg += b[0:2]
            b = b[2:]
            # print b
            # 05
            print ("jsjsjsj", b[0:2])
            mobile_id_length = int(b[0:2])
            # print mobile_id_length
            #ack_msg += b[0:2]
            b = b[2:]
            # print b
            # 4864037022 mobile Id
            #print ("parse_data", parse_data)
            parse_data.update({"mobile_id_length": mobile_id_length})
            #print (parse_data['mobile_id_length'], b[0:mobile_id_length*2], mobile_id_length)
            parse_data.update(
                {"mobile_id": (b[0:mobile_id_length*2])})
            #ack_msg += b[0:mobile_id_length*2]
            b = b[mobile_id_length*2:]
            # print b
            # 01 Mobile Type Length
            #ack_msg += b[0:2]
            mobile_id_type_length = int(b[0:2], 16)
            b = b[2:]
           
            parse_data.update({"mobile_id_type": int(
                b[0:mobile_id_type_length*2], 16)})
            #ack_msg += b[0:2]
            b = b[mobile_id_type_length*2:]
           
            parse_data.update({"service_type": int(b[0:2], 16)})
            b = b[2:]
            
            parse_data.update({"message_type": int(b[0:2], 16)})
            b = b[2:]
            #print ("parse_data", parse_data)
            # 0102  Dont Know
            b = b[4:]
            # print b
            parse_data.update({"update_time": int(b[0:8], 16)})
            b = b[8:]
            # print b
            parse_data.update({"time_of_fix": int(b[0:8], 16)})
            b = b[8:]
            # print "latitude", b[0:8]
            parse_data.update(
                {"latitude": self.get_value_from_2compli(b[0:8])/10000000.0000000000})
            b = b[8:]
            # print "longitude", b[0:8]
            parse_data.update(
                {"longitude": self.get_value_from_2compli(b[0:8])/10000000.000000000})
            b = b[8:]
            # print "inpur las", b
            parse_data.update(
                {"altitude": self.get_value_from_2compli(b[0:8])/10000000.0000000000})
            b = b[8:]
            parse_data.update({"speed": int(b[0:8], 16)})
            b = b[8:]
            parse_data.update({"heading": int(b[0:4], 16)})
            b = b[4:]
            parse_data.update({"satellites": int(b[0:2], 16)})
            b = b[2:]
            parse_data.update({"fix_status": int(b[0:2], 16)})
            b = b[2:]
            parse_data.update({"carrier": int(b[0:4], 16)})
            b = b[4:]
            parse_data.update({"RSSI": int(b[0:4], 16)})
            b = b[4:]
            parse_data.update({"com_states": int(b[0:2], 16)})
            b = b[2:]
            parse_data.update({"hdop": int(b[0:2], 16)})
            b = b[2:]
            #print ("parse_data", parse_data)
            #print (parse_data)
            #
        except Exception as e:
            print (str(e))

        try:
            cursor = self.conn.get_connection()
            s = "insert into gps_tracking(`device_id`, `latitude`, `longitude`,\
             `speed`,`update_time`,`time_of_fix`, \
             `altitude`,`heading`, `satellites`,\
              `fix_status`, `carrier`, `rssi`,\
              `com_states`, `hdop`, `packet`, `entry_time`) values('%s', %s,%s, %s, %s, %s, %s,%s, %s,%s, %s, %s, '%s', %s, '%s','%d')"\
              % (parse_data['mobile_id'], parse_data['latitude'], parse_data['longitude'],
                parse_data['speed'], parse_data['update_time'], parse_data['time_of_fix'],
                parse_data['altitude'], parse_data['heading'], parse_data['satellites'],
                parse_data['fix_status'], parse_data['carrier'], parse_data['RSSI'],
                parse_data['com_states'], parse_data['hdop'], binary_data,int(time.time()) )
            #print (s)
            cursor.execute(s)
        except Exception as e:
            print (str(e))


