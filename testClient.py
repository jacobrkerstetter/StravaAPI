import socket
import time

s = socket.socket()

# server info
host = '10.0.0.131'
port = 8090

print('Connecting to server...')

# connect and send test data
s.connect((host, port))
print('Connected')

message = 'Hello World'
s.send(message.encode())
print('Data sent')

# receive data echo
print('Reading data')
data = ''
while len(data) < len(message):
    data += s.recv(1).decode('utf-8')
    time.sleep(1)

print(data)
s.close()