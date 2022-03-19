import queue

from threading import Thread

class ThreadPool:

    def __init__(self, nthreads, function):
        self.nthreads = nthreads
        self.function = function
        self.queue = queue.Queue(nthreads)
        self.is_running = False
        self.threads = [
            Thread(target=self._target)
            for _ in range(self.nthreads)
        ]

    def start(self):
        self.is_running = True
        for thread in self.threads:
            thread.start()

    def push(self, args):
        self.queue.put(args)

    def stop(self):
        self.queue.join()
        self.is_running = False
        for thread in self.threads:
            thread.join()

    # internal

    def _target(self):
        while self.is_running:
            args = self.queue.get(block=True)
            self.function(*args)
            self.queue.task_done()
