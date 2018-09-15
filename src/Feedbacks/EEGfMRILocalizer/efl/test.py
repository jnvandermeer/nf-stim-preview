from multiprocessing import Process
import multiprocessing

def f(name):
    print 'hello', name

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
	
	
	
	
class testMp(multiprocessing.Process):
        
		
    def __init__(self,var):

        super(testMp, self).__init__()
        self.var=var

		
    def run(self):
        print('hallo')
            
            
    def send_message(self,message):
        '''
        it'll put the message into the queue, to be processed by 'run'
        '''
        self._queue.put(message)
		

if __name__ == "__main__":		
    t=testMp('var')

    t.start()
    t.join()
