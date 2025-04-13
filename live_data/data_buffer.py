from collections import deque
import pandas as pd
import threading

class DataBuffer:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.lock = threading.Lock()
        
    def add(self, data):
        with self.lock:
            self.buffer.append(data)
            
    def snapshot(self, as_dataframe=True):
        with self.lock:
            if as_dataframe:
                return pd.DataFrame(self.buffer)
            return list(self.buffer)
