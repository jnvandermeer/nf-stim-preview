import socket

def Main():
    
    #host='127.0.0.1'
    host='10.1.121.28'
    # host='10.1.121.28'
    port=5001
    
    #server=('10.1.125.11', 5000)
    #server=('127.0.0.100', 5000)
    server=('10.1.125.11', 5000)
    # server=('127.0.0.1', 5000)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    s.bind((host,port))
    # so you bind to THIS 'server'?
    
    
    while True:
    
        message = raw_input("-> ")

        s.sendto(message, server)
        if str(message) == 'q':
            break
        data, addr = s.recvfrom(1024)
        print "Received from server: " + str (data)
        print "Address was: " + str(addr)

    # here, closing off the socket will NOT shut off the server!! Since the UDP stays 'alive'! 
    s.close()
    
if __name__ == '__main__':
    Main()
