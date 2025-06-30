class ConstantArg:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Constant({self.value})"


class BlockArg:
    def __init__(self, block_id):
        self.block_id = block_id
    
    def __repr__(self):
        return f"Block('{self.block_id}')"