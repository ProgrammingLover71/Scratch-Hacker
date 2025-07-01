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


class VariableArg:
    def __init__(self, var):
        self.var = var
    
    def __repr__(self):
        return f"Variable('{self.var}')"
