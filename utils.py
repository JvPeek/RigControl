import serial.tools.list_ports
import time

def getAvailablePorts():
    ports = serial.tools.list_ports.comports()

    return list(map( lambda thing: thing.device , sorted(ports)))


def mapRange(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getTimeAsMS():
    return int(round(time.time() * 1000))