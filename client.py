import socket

Format = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((socket.gethostname(), 5545))
except socket.timeout:
    exit(0)

reply = client.recv(1024).decode()
print(reply)

# Sends prompt about email
while True:
    user_input = input(">>> ")
    client.send(user_input.encode())
    payload = client.recv(1024).decode()
    print(f'Message from Server... \n{payload}')
    
    


    