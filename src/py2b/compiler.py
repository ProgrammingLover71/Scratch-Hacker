import ast

source = """
def main():
    my_var = (1.0 + 1.0)
    my_var += my_var
"""

tree = ast.parse(source)
print(ast.dump(tree, indent=4))