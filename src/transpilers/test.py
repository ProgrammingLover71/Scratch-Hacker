from python_to_blocks import PythonToBlocks, ast
from json import dumps

code = """
@when_flag_clicked
def main():
    my_var = 1 + 1
    my_var += 2
"""

p2b = PythonToBlocks()
result = dict(p2b.visit(ast.parse(code)))
for block_id, block in result.items():
    print(f"{block_id}: {dumps(block, indent=4)}")
    