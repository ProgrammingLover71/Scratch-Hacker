from project_reader import ProjectReader
from transpilers.blocks_to_python import BlocksToPython
from transpilers.python_to_blocks import PythonToBlocks

DEBUG_TEST_READER_B2PY = True

# Main entry point for the script
# This script reads a Scratch project file and converts its blocks to Python code.
if __name__ == "__main__" and DEBUG_TEST_READER_B2PY:
    # Initialize the project reader
    project_reader = ProjectReader('./test_project.sb3')
    # Read the blocks from the project
    project_blocks = project_reader.get_blocks()
    # Convert the blocks to Python code
    output_python = BlocksToPython().get_python_from_blocks(project_blocks)
    # Write the output to a file
    with open('output.py', 'w', encoding='utf-8') as output_file:
        output_file.write(output_python) 