import ast
from py2b_utils import *

# This class is responsible for converting Python code into a block-based representation.
# It uses the `ast` module to parse the Python code and generate blocks that represent the
# structure and logic of the code.
class PythonToBlocks(ast.NodeVisitor):
    def __init__(self):
        self.blocks = {}
        self.variables = {}  # To keep track of variable names
        self.next_id = 0
        self.flag_click_block_id = ''
        self.block_chain = BlockChain()  # To keep track of the block chain
    
    # Returns an ID for a new block.
    # This ID is a string that starts with "block_" followed by an incrementing number.
    def new_id(self):
        self.next_id += 1
        return f"block_{self.next_id}"
    
    
    # This method is called when the root module of the Python code is encountered.
    # It iterates through all the statements in the module body and visits each statement.
    # It returns the blocks generated from the statements.
    # The blocks are stored in the `self.blocks` dictionary, which maps block IDs to
    # their properties such as opcode, inputs, next block ID, parent block ID, fields, and topLevel status.
    # The `visit` method is a generic method that calls the appropriate visit method based on
    # the type of the node (statement) it receives.
    def visit_Module(self, node):
        for statement in node.body:
            self.visit(statement)
        return self.blocks
    

    # This method is called when a variable assignment is encountered in the Python code.
    # It generates a block that represents the assignment operation.
    # The block is created with the opcode 'data_setvariableto', which is used to
    # set the value of a variable in the block-based representation.
    def visit_Assign(self, node: ast.Assign):
        target = node.targets[0].id
        block_id = self.new_id()
        self.expr_parent_id = block_id  # Set the parent ID for expressions
        value = self.visit(node.value)
        self.block_chain.add(BlockNode({
            'opcode': 'data_setvariableto',
            'inputs': {
                'VALUE': self.create_input(value),
            },
            'next': None,
            'parent': None,
            'fields': {
                'VARIABLE': [target, target]
            },
            'topLevel': False
        }))
        self.variables[f'var_{target}'] = [target, 0]
    
    # This method is called when an augmented assignment statement is encountered in the Python code.
    # It generates a block that represents the operation.
    # The block is created with the opcode 'data_changevariableby', which is used to
    # change the value of a variable in the block-based representation.
    def visit_AugAssign(self, node):
        target = node.target.id
        block_id = self.new_id()
        self.expr_parent_id = block_id  # Set the parent ID for expressions
        value = self.visit(node.value)  # Get the value of the augmented assignment
        op = node.op
        opcode = 'data_changevariableby'
        if isinstance(op, ast.Add):
            pass
        elif isinstance(op, ast.Sub):
            inp_id = self.new_id()
            idx = self.block_chain.add(BlockNode(self.make_binop(ConstantArg(0), value, 'operator_subtract')))
            value = BlockArg(inp_id)  # Use the binop block as the value
        else:
            raise ValueError(f"Unsupported augmented assignment operation: {ast.dump(op)}")
        self.block_chain.add(BlockNode({
            'opcode': opcode,
            'inputs': {
                'VALUE': self.create_input(value)
            },
            'next': None,
            'parent': None,
            'fields': {
                'VARIABLE': [target, target]
            },
            'topLevel': False
        }))
        return BlockArg(block_id)  # Return a BlockArg for the block ID
    

    # This method is called when a binary operation (like addition, subtraction, etc.) is encountered in the Python code.
    # It generates a block that represents the operation.
    # The block is created with the appropriate opcode based on the operation type.
    # The inputs for the block are the left and right operands of the operation.
    def visit_BinOp(self, node):
        left = self.visit(node.left)  # Visit the left operand
        right = self.visit(node.right)  # Visit the right operand
        op = node.op
        opcode = ''
        if isinstance(op, ast.Add):
            opcode = 'operator_add'
        elif isinstance(op, ast.Sub):
            opcode = 'operator_subtract'
        elif isinstance(op, ast.Mult):
            opcode = 'operator_multiply'
        elif isinstance(op, ast.Div):
            opcode = 'operator_divide'
        else:
            raise ValueError(f"Unsupported binary operation: {ast.dump(op)}")
        block_id = self.new_id()
        self.blocks[block_id] = self.make_binop(left, right, opcode)
        self.add_block(block_id, is_stack_block=False)
        return BlockArg(block_id)  # Return a BlockArg for the block ID
    

    def make_binop(self, left, right, opcode):
        return {
            'opcode': opcode,
            'inputs': {
                'NUM1': self.create_input(left),
                'NUM2': self.create_input(right)
            },
            'next': None,
            'parent': None,
            'fields': {},
            'topLevel': False
        }

    
    # This method is called when a function definition is encountered in the Python code.
    # It checks if the function is named 'main' and if it has the `when_flag_clicked` decorator.
    # If so, it creates a block for the main function and sets the flag click block ID for later use.
    # If the function is not named 'main', it raises a ValueError.
    def visit_FunctionDef(self, node):
        name = node.name
        block_id = self.new_id()
        if name == 'main':
            # Special handling for the main function
            # We need to check if the function is decorated with `when_flag_clicked`
            if any(decorator.id == 'when_flag_clicked' for decorator in node.decorator_list):
                self.flag_click_block_id = block_id   # Set the flag click block ID for later use
                self.add_block(block_id, is_stack_block=True)
                self.blocks[block_id] = {
                    'opcode': 'event_whenflagclicked',
                    'inputs': {},
                    'next': None,
                    'parent': None,
                    'fields': {},
                    'topLevel': True,
                    'x': 100,
                    'y': 100
                }
                self.generic_visit(node)  # Visit the function body
        else:
            raise ValueError(f"Non-main functions are not supported: '{name}'")
    

    # This method is called when a constant value is encountered in the Python code.
    # It returns the value of the constant, which can be a number or a string.
    # If the constant is NOT a number or a string, it raises a ValueError.
    # This is to ensure that only valid Scratch constant values are processed.
    def visit_Constant(self, node):
        if isinstance(node.value, (bool, int, float, str)):
            return ConstantArg(node.value)
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")


    # This method is called when a block ID is added to the list of block IDs.
    # It appends the block ID to the `self.block_ids` list, which keeps track of all block IDs generated during the parsing process.
    # This is useful for later reference or for generating the final project structure.
    def add_block(self, block_id, is_stack_block=True):
        self.block_ids.append((block_id, is_stack_block))


    # This method is called to retrieve the last stack block ID from the list of block IDs.
    # It iterates through the list in reverse order and returns the first block ID that is a stack block (i.e., `is_stack_block` is True).
    # This is useful for identifying the last stack block in the sequence of blocks.
    def get_last_stack_block_id(self):
        for block_id, is_stack_block in reversed(self.block_ids):
            if is_stack_block:
                return block_id

    # This method is called when parsing an input value for a block.
    # It checks if the value is a ConstantArg or a BlockArg and returns the appropriate
    # representation for the block input.
    # If the value is not a ConstantArg or BlockArg, it raises a ValueError.
    def create_input(self, value):
        if isinstance(value, ConstantArg):
            return [1, [10, value.value]]
        elif isinstance(value, BlockArg):
            return [3, value.block_id]
        else:
            raise ValueError(f"Unsupported input type: {type(value).__name__} (value: {value})")
    