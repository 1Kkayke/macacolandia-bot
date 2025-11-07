"""Music queue management"""

from collections import deque
import random


class MusicQueue:
    """Manages the music queue for a guild"""
    
    def __init__(self):
        self.queue = deque()
        self.current = None
        self.volume = 0.5

    def add(self, song):
        """Add a song to the queue"""
        self.queue.append(song)

    def get_next(self):
        """Get the next song from the queue"""
        if self.queue:
            self.current = self.queue.popleft()
            return self.current
        return None

    def clear(self):
        """Clear the queue and current song"""
        self.queue.clear()
        self.current = None

    def shuffle(self):
        """Shuffle the queue"""
        temp_list = list(self.queue)
        random.shuffle(temp_list)
        self.queue = deque(temp_list)

    def is_empty(self):
        """Check if the queue is empty"""
        return len(self.queue) == 0

    def size(self):
        """Get the size of the queue"""
        return len(self.queue)
