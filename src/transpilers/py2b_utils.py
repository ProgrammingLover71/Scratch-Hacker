class ConstantArg:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if isinstance(other, ConstantArg):
            return self.value == other.value
        return False

    def __sub__(self, other):
        if isinstance(other, ConstantArg):
            return ConstantArg(self.value - other.value)
        return NotImplemented
    
    def __neg__(self):
        return ConstantArg(-self.value)
    
    def __repr__(self):
        return f"Constant({self.value})"


class BlockArg:
    def __init__(self, block_id):
        self.block_id = block_id
    
    def __repr__(self):
        return f"Block('{self.block_id}')"
    

# This class represents a node in the block chain.
# It contains data and a reference to the next node.
# The BlockChain class manages a linked list of BlockNode instances.
class BlockNode:
    def __init__(self, data, next: 'BlockNode' = None):
        self.data = data
        self.next = next
    
    def __repr__(self):
        return f"BlockNode(data={self.data}, next={self.next})"


# This class represents a linked list of blocks in the blockchain.
# It allows adding new blocks and maintains references to the head and tail of the list.
# Each block is represented by a BlockNode instance.
class BlockChain:
    
    # Initializes an empty block chain with head, tail, and length attributes.
    # The head and tail are set to None, and the length is initialized to 0.
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    
    # Adds a new block to the end of the chain.
    # Increments the length of the chain and updates the head and tail references.
    def add(self, data: BlockNode):
        new_node = data
        self.length += 1
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return self.length

    # Returns the block at the specified index.
    # Raises IndexError if the index is out of range.
    def __index__(self, index):
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current
