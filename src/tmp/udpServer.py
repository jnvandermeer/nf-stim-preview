import socket

def Main():
    host='127.0.0.1'
    port=5000
    
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    s.bind(('', port))
    
    print "Server started "
    
    while True:
        data, addr = s.recvfrom(2014)
        if str(data) == 'q':
            break
        print "message from: " + str (addr)
        print "from connected user: " + str(data)
        data = str(data).upper()         
        print "sending: " + str(data)
        s.sendto(data, addr)
        
    s.close()
    
if __name__ == "__main__":
    Main()
    
    
    
        