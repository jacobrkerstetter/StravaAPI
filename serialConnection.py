import serial

# setup
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/cu.usbserial-D30DPGM0'
ser.open()

# writing 
vals = bytearray([20, 40, 60])
ser.write(vals)

# reading
totalBytes = 0
while totalBytes < len(vals):
    print(ord(ser.read()))
    totalBytes += 1