class Queue:
    # Constructor
    def __init__(self, size=1000):  # Set size to 1000
        self.q = [None] * size      # Using list to store elements of Queue
        self.capacity = size        # Maximum capacity of the Queue
        self.front = 0              # 1st element in the Queue
        self.rear = -1              # Last element in the Queue
        self.count = 0              # Current size of the Queue

    # Function to dequeue the front element
    def dequeue(self):
        # check for queue underflow
        if self.isEmpty():
            print('Queue is underflow, terminating process...')
            exit(-1)
        x = self.q[self.front]
        # print('Removing element…', x)
        self.front = (self.front + 1) % self.capacity
        self.count = self.count - 1
        return x

    # Function to add an element to the queue
    def enqueue(self, value):
        # check for queue overflow
        if self.isFull():
            print('Queue is overflow, terminating process...')
            exit(-1)
        # print('Inserting element…', value)
        self.rear = (self.rear + 1) % self.capacity
        self.q[self.rear] = value
        self.count = self.count + 1

    # Function to return the front element of the Queue without removing from Queue
    def peek(self):
        if self.isEmpty():
            print('Queue is underflow, terminating process...')
            exit(-1)
        return self.q[self.front]

    # Function to return the size of the Queue
    def size(self):
        return self.count

    # Function to check if the Queue is empty
    def isEmpty(self):
        return self.size() == 0

    # Function to check if the Queue is full
    def isFull(self):
        return self.size() == self.capacity