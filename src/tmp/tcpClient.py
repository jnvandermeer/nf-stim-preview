import socket

def Main():
    #host='127.0.0.1'
    host='10.1.121.28'
    # host='172.16.11.253'
    port=5000
    
    s=socket.socket()
    s.connect((host,port))
    
    message = raw_input("-> ")
    
    while message != 'q':
        
        s.send(message)
        
        data=s.recv(1024)
        
        print "Received from server: " + str(data)
        message = raw_input("-> ")
        
    # here, closing of the socket will also shut off the server. Until there's a new 'listening' operation planned.
    s.close()
    
if __name__ == '__main__':
    Main()
    
    