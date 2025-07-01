from python_to_blocks import PythonToBlocks, ast
from project_maker import ProjectMaker

code = """
x = 5
x += 2
x -= 3 + 1
y = 17 / 3
y += 16 / 7
y -= 23 / (9 + x)
"""

def main():
    # Create an instance of the PythonToBlocks class
    transpiler = PythonToBlocks()
    
    # Parse the Python code and generate blocks
    transpiler.visit(ast.parse(code))
    
    # Create a project maker instance
    project_maker = ProjectMaker()
    
    # Create the project JSON structure with the generated blocks and variables
    project_json = project_maker.create_project_json({
        'blocks': transpiler.blocks,
        'variables': transpiler.variables,
        'name': 'MySprite'
    })
    
    #with open('project.json', 'w') as f:
    #    import json
    #    json.dump(project_json, f, indent=4)
    # Save the project JSON to a file
    project_maker.save_project(project_json, 'project.sb3')

if __name__ == "__main__":
    main()