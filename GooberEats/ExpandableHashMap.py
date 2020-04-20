"""
For simplicity, maximum capacity of 25969 (12th prime in the list) was used as

Load Factor = # of items to insert / hash table size
# of items to insert = 0.5 * 25969 = 12984.5 

which is much greater than the expected number of insertions
The capacity of the hash table will be capped at the last prime of 25969
"""
PRIME_NUMBER_COUNT = 12

# list of prime that roughly doubles (to be used to increase capacity of hash table)
# after the first rehash which will increase table size from 8 to 11, 
# it will roughly double (11 -> 23 -> 47 -> ... -> 25969)
primeNumberList = [11, 23, 47, 97, 199, 397, 797, 1597, 3191, 6389, 12781, 25969]

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def hasKey(self, key):
        return self.key == key

class ExpandableHashMap:

    def __init__(self, maxLoadFactor = 0.5):
        self.__size = 0
        self.__capacity = 8
        self.__indexOfNextPrime = 0
        self.__loadFactor = 0.0
        self.__maxLoadFactor = maxLoadFactor if maxLoadFactor > 0 else 0.5
        self.__table = [[] for _ in range(self.__capacity)]

    # magic method to support value = ExpandableHashMap[key]
    def __getitem__(self, key):
        return self.find(key)

    # magic method to support ExpandableHashMap[key] = value
    def __setitem__(self, key, value):
        self.associate(key, value)

    # resets the hashmap back to 8 buckets, deletes all items    
    def reset(self):
        self = ExpandableHashMap(self.__maxLoadFactor)

    # returns the number of associations in the hashmap
    def size(self):
        return self.__size
    
    # Inserts a key, value pair into the hash table (value will be updated if key already exists).
    # @param key The key of the association to be inserted.
    # @param value The value (of the key) of the association to be inserted.
    # @post If key currently does not exist in the hash table, the key, value pair will 
    #   be inserted into the hash table. If it already exists, its value will be updated.
    def associate(self, key, value):
        row, col = self.__findIndices(key)
        if row is not None:
            self.__table[row][col].value = value
            return
        bucket = self.__hash(key)
        self.__table[bucket].append(HashNode(key, value))
        self.__size += 1
        self.__updateLoadFactor()
        if (self.__loadFactor > self.__maxLoadFactor):
            self.__rehash()

    # Finds the value of a key.
    # @param key The key whose value is to be returned.
    # @return None if key is not found, else its value.
    def find(self, key):
        row, col = self.__findIndices(key)
        return None if row is None else self.__table[row][col].value

    # A private function that returns the row and column indices of a key.
    # @param key The key whose row and column is to be found (and returned).
    # @return A pair consisting of None, None if key is not found, else its row, column.
    def __findIndices(self, key):
        row = self.__hash(key)
        if (len(self.__table[row]) == 0):
            return None, None
        for node in self.__table[row]:
            if node.hasKey(key): 
                return row, self.__table[row].index(node)
        return None, None
    
    # A private function that returns a hash value of a key.
    # @param key The key of which to compute the hash value.
    # @return The computed hash value of range [0, sizeOfTable]
    def __hash(self, key):
        return hash(key) % self.__capacity
    
    # A private function that rehashes the whole table, roughly doubling its capacity.
    # @post The hash table shall have all its keys rehashed and its size will be roughly doubled.
    def __rehash(self):
        if (self.__indexOfNextPrime >= PRIME_NUMBER_COUNT):
            return
        
        newCapacity = primeNumberList[self.__indexOfNextPrime]
        self.__indexOfNextPrime += 1

        # create a new empty table with increased size while keeping a copy of 
        # old table to be rehashed
        oldTable        = self.__table
        self.__table    = [[] for _ in range(newCapacity)]
        self.__capacity = newCapacity
        # update size to 0 as it will be increased when reinserting associations
        self.__size     = 0 

        for bucket in oldTable:
            for hashnode in bucket:
                self.associate(hashnode.key, hashnode.value)

        self.__updateLoadFactor()

    # A private function that updates the hash table's load factor.
    def __updateLoadFactor(self):
        self.__loadFactor = self.__size / self.__capacity