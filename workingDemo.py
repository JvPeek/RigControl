## init
##0x01 0x01 0x02 0x00 0x00 0x02

## turn
##0x11 0x02 0x02 0x00 0x10 0x01

## turn back
##0x11 0x03 0x02 0xFF 0xF0 0x1F
##
##pip install pyserial


import time
import serial
import threading

running = True

def read_serial_function(name):
    while running:
        cmd = ord(arduino.read(size=1))
        id = ord(arduino.read(size=1))
        size = ord(arduino.read(size=1))
        buf = []
        i =0
        while i < size:
            buf.append(arduino.read(size=1))
            i = i+1
        checksum = ord(arduino.read(size=1))

        if cmd==0x74:
            print ("helo")
        elif cmd==0xfe:
            print ("debug: ", end='')
            for b in buf:
                print(b.decode("ascii"), end='')
            print("")    
        elif cmd==0xf0:
            print ("ACK: ", end='')
            if ord(buf[0]) == 0x00:
              print ("OK")
            elif ord(buf[0]) == 0x01:
              print ("Parameter error")
            elif ord(buf[0]) == 0x02:
              print ("Wrong checksum")
            elif ord(buf[0]) == 0x03:
              print ("Not in interface mode")
            else:
              print ("unknown status", end='')
              print (hex(ord(buf[0])))
        else:
            print("cmd ", end='')
            print(hex(cmd), end='')
            print(", id ", end='')
            print(hex(id), end='')
            print(", size ", end='')
            print(size, end='')
            print(", buf ", end='')
            for b in buf:
                print(hex(ord(b)), end='')
            print(", checksum ", end='')
            print(hex(checksum), end='')
            print("")    





if __name__ == "__main__":

    try:
        arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
        #arduino = serial.Serial(port='COM3', baudrate=115200)
        
        # toggle DTR to reset arduino
        arduino.dtr = not(arduino.dtr)
        time.sleep(0.1)
        # and back
        arduino.dtr = not(arduino.dtr)
        
        ## start the answer debug thread
        x = threading.Thread(target=read_serial_function, args=(1,))
        x.start()

        # wait for arduino to boot
        time.sleep(2)
    
        print("initializing")
        packet= bytearray()
        packet.append(0x01)
        packet.append(0x01)
        packet.append(0x02)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x02)
        arduino.write(packet)

        time.sleep(0.2)

        print("turn left")
        packet= bytearray()
        packet.append(0x11)
        packet.append(0x02)
        packet.append(0x02)
        packet.append(0x00)
        packet.append(0x01)
        packet.append(0x10)
        arduino.write(packet)

        time.sleep(3)

        print("turn right")
        packet= bytearray()
        packet.append(0x11)
        packet.append(0x03)
        packet.append(0x02)
        packet.append(0xFF)
        packet.append(0xFF)
        packet.append(0x10)
        arduino.write(packet)

        time.sleep(3)

        print("stop")
        packet= bytearray()
        packet.append(0x11)
        packet.append(0x02)
        packet.append(0x02)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x11)
        arduino.write(packet)

        # 10 more secs of debug output
        time.sleep(10)
        running=False
        
    except KeyboardInterrupt:
        running=False
    
