import socket

# Our Google Cloud VM at the moment has an ephemeral external IP Address
# It basically will change everytime we stop and run it
# IF we need it, we can try to set up a static IP address
#ADDRESS = "35.236.32.223"

# The Google Cloud VM will allow any connection from this port
#PORT = 3389
()
if __name__ == "__main__":
    address = input('Enter address: ')
    port = int(input('Enter port: '))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))

    # This simply sends an encoded string to the server
    # The server will then send the same string but backwards to us
    # This is proof that the VM can get our information, modify it, and send it back to us
    message = input("Enter message: ") 
    while message.lower().strip() not in ['exit', 'end', 'quit', 'stop']: # Stop words
        sock.send(message.encode()) 
        data = sock.recv(4096).decode() 
        print(data)

        message = input("Enter message: ") 

    sock.close()