import serial
import struct
import time

angles = [0, 10, 20]
speeds = [-250,0,255]
arduino = serial.Serial('/dev/ttyACM0', timeout=1, baudrate=9600)
time.sleep(3) # Arduino will be reset when serial port is opened, wait it to boot

def calc_checksum(data):
    calculated_checksum = 0
    for byte in data:
        calculated_checksum ^= byte
    return calculated_checksum

def read_packet():
    '''
    :return received data in the packet if read sucessfully, else return None
    '''
    # check start sequence
    if arduino.read() != b'\x10':
        return None

    if arduino.read() != b'\x02':
        return None

    payload_len = arduino.read()[0]
    if payload_len != 9:
        # could be other type of packet, but not implemented for now
        return None

    # we don't know if it is valid yet
    payload = arduino.read(payload_len)

    checksum = arduino.read()[0]
    if checksum != calc_checksum(payload):
        return None # checksum error

    # check end sequence
    if arduino.read() != b'\x10':
        return None
    if arduino.read() != b'\x03':
        return None    

    # yeah valid packet received
    return payload

def send_packet():
    tx = b'\x10\x02' # start sequence
    tx += struct.pack("<B", 9) # length of data
    packed_data = struct.pack("<BBBhhh", *angles, *speeds)
    tx += packed_data
    tx += struct.pack("<B", calc_checksum(packed_data))
    tx += b'\x10\x03' # end sequence
    print("Sending:", tx.hex())
    arduino.write(tx)

def main():
    timeout = 3
    try:
        # keep sending packet and try to unpack received packet
        while True:
            print("Setting angle outputs", angles) # first 3 unpacked values
            print("Setting speed outputs", speeds) # next 3 unpacked values
            send_packet()
            time.sleep(0.5)

            start_time = time.time()
            payload = None
            while(payload == None and time.time() < (start_time+timeout)):
                payload = read_packet()
            if payload == None:
                print("timeout")
                continue
            # a packet is read successfully
            unpacked = struct.unpack("<BBBhhh", payload)
            print("Actual angle outputs", unpacked[:3]) # first 3 unpacked values
            print("Actual speed outputs", unpacked[3:]) # next 3 unpacked values

            print("\n\n")
    except KeyboardInterrupt:
        exit(0)

main()