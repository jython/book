class WorkQueue(object):

    def worker(self):
        while self._running:
            self._queue.get()()
            self._queue.task_done()
    
    def __init__(self, queue):
        self._queue = queue
        self._running = True
        for i in range(num_worker_threads):
            Thread(target=self.worker).start()
        
    def shutdown(self):
        self._running = False
        self._queue.join()
    
        


q = Queue()

for item in source():
    q.put(item)

q.join()     
