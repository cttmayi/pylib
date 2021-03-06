
import time
 
class Perf:
    def __init__(self, label):
        self.label = label
 
    def __enter__(self):
        self.start = time.time()
 
    def __exit__(self, exc_ty, exc_val, exc_tb):
        end = time.time()
        print('{}: {}'.format(self.label, end - self.start))
 
with Perf('Counter'):
    n = 10000000
    while n > 0:
        n -= 1
 
# counting: 1.36000013351