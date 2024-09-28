class Stack:
	# Initializing stack a the given capacity
	def __init__(self, cap=10):
		self.cap = cap
		self.stack = [None] * cap
		self.top = -1
		
	
	def capacity(self):#return the capacity of the stack
		return self.cap

	def push(self, data): #add the given data to the stack
		if self.top + 1 >= self.cap:
			self.cap *=2
			new_stack = [None] * self.cap
			for i in range(self.top + 1):
				new_stack[i] = self.stack[i]
			self.stack = new_stack
		self.top += 1
		self.stack[self.top] = data


		
	def pop(self): # remove the first element of the stack (last added element)
		if self.top == -1:
			raise IndexError("pop() used on empty stack")
		popped_element = self.stack[self.top]
		self.stack[self.top] = None
		self.top -=1
		#self.size -=1
		return popped_element
	
	def get_top(self): # return the first element of the stack without removing from the stack
		if self.top == -1:
			return None
		return self.stack[self.top]

	def is_empty(self): #return true if the stack is empty
		return self.top == -1


	def __len__(self): #return the current length of the stack
		return self.top + 1

	def display(self): # for testing purposes
		for i in range(self.top + 1):
			print(self.stack[i])
	


class Queue:
	
	def __init__(self, cap= 10): #initialize the queue with the given capacity
		self.cap = cap
		self.queue = [None] * cap
		self.front = 0
		self.back  = -1
		self.size  = 0


	def capacity(self): #Returns the capacity of the queue
		return self.cap

	def enqueue(self, data): # adding one element to the queue
		if self.size >= self.cap:
			self.resize(2 * self.cap)
   
		self.back = (self.back + 1)% self.cap
		self.queue[self.back] = data
		self.size +=1
  
  
	def dequeue(self): # Remove the added element from the queue
		if self.is_empty():
			raise IndexError("dequeue() used on empty queue")

		data = self.queue[self.front]
		self.queue[self.front] = None
		self.front = (self.front + 1) % self.cap
		self.size -= 1
		return data

			

	def get_front(self): # return the first added element of the queue without removing it from the queue
		if self.size == 0:
			return None
		return self.queue[self.front]
			

	def is_empty(self): # returns true if queue has 0 element
		return self.size == 0

	def __len__(self): # return the actual length of the queue
		return self.size 

	def resize(self, new_cap):
		new_queue = [None] * new_cap
	
		for i in range(self.size):
			new_queue[i] = self.queue[(self.front + i) % self.cap]
		self.queue = new_queue
		self.front = 0
		self.back  = self.size - 1
		self.cap = new_cap
	

	def display(self): #for testing purposes
		if self.size > 0:
			for i in range(self.size+1):
				print(self.queue[i])
		
	def get_back(self): #for testing purposes
		return self.queue[self.back]
    
    
class Deque:

	def __init__(self, cap = 10):
		self.cap = cap
		self.front = 0
		self.back = -1
		self.size = 0
		self.deque = [None] * cap


	def capacity(self):
		return self.cap

	def push_front(self, data):
		if self.size >= self.cap:
			self.resize(2 * self.cap)

		self.front = (self.front - 1) % self.cap
		self.deque[self.front] = data
		self.size += 1

	def push_back(self, data):
		if self.size >= self.cap:
			self.resize(2 * self.cap)

		self.back = (self.back + 1) % self.cap
		self.deque[self.back] = data
		self.size += 1

  

	def pop_front(self):
		if self.is_empty():
			raise IndexError('pop_front() used on empty deque')

		data = self.deque[self.front]
		self.deque[self.front] =None
		self.front = (self.front + 1) % self.cap
		self.size -= 1
		return data

  

	def pop_back(self):
		if self.is_empty():
			raise IndexError('pop_back() used on empty deque')

		data = self.deque[self.back]
		self.deque[self.back] = None
		self.back = (self.back - 1) % self.cap
		self.size -= 1
		return data



	def get_front(self):
		if self.is_empty():
			return None

		return self.deque[self.front]

	def get_back(self):
		if self.is_empty():
			return None

		return self.deque[self.back]

	def is_empty(self):
		return self.size == 0

	def __len__(self):
		return self.size
		

	def __getitem__(self, k):
		if k < 0 or k >=self.size:
			raise IndexError('Index out of range')

		index = (self.front + k) % self.cap
		return self.deque[index]


	def resize(self, new_capacity):
		new_deque = [None] * new_capacity
		for i in range(self.size):
			new_deque[i] = self.deque[(self.front + i) % self.cap]
		self.deque = new_deque
		self.front = 0
		self.back = self.size - 1
		self.cap = new_capacity

