import ast

class PythonToBlocks(ast.NodeVisitor):
    def __init__(self, py_code: str):
        self.py_code = py_code
        self.blocks = []
    