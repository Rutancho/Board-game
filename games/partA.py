#    Main Author(s): Ziyang Wang, Wilgard Fils-aime, Jaehyuk Heo
#    Main Reviewer(s):Jaehyuk Heo

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        
    def insert1(self, key, value):
        if self.find(key) is not None:
            return False
        new_node = Node(key, value)
        new_node.next = self.head
        self.head = new_node
        return True 
    
    def find(self, key):
        current = self.head 
        while current:
            if current.key == key:
                return current
            current = current.next
        return None
    
    def modify(self, key, value):
        node = self.find(key)
        if node is None:
            return False
        node.value = value
        return True
    
    def remove(self, key):
        current = self.head
        previous = None
        while current:
            if current.key == key:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

class HashTable:
    def __init__(self, cap=32):
        self.cap = cap 
        self.size = 0
        self.table = [LinkedList() for _ in range(self.cap)]

    def insert(self, key, value):
        index = hash(key) % self.cap
        if self.table[index].insert1(key, value):
            self.size += 1
            if self.size / self.cap > 0.7:
                new_cap = self.cap * 2
                new_table = [LinkedList() for _ in range(new_cap)]
                for linked_list in self.table:
                    current = linked_list.head
                    while current:
                        new_index = hash(current.key) % new_cap
                        new_table[new_index].insert1(current.key, current.value)
                        current = current.next
                self.table = new_table
                self.cap = new_cap
            return True
        return False


    def modify(self, key, value):
        index = hash(key) % self.cap
        if self.table[index].modify(key, value):
            return True
        return False

    def remove(self, key):
        index = hash(key) % self.cap
        if self.table[index].remove(key):
            self.size -= 1
            return True
        return False

    def search(self, key):
        index = hash(key) % self.cap
        node = self.table[index].find(key)
        return node.value if node else None

    def capacity(self): 
        return self.cap

    def __len__(self):
        return self.size


        
