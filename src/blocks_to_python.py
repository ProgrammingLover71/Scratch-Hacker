from util_classes import Variable, Block
from typing import List

class BlocksToPython:

    # Converts a list of blocks to Python code.
    # This method assumes that the blocks are of type Block for simplicity.
    @staticmethod
    def get_python_from_blocks(blocks: List[Block]) -> str:
        python_code = ""
        for block in blocks:
            if isinstance(block, Variable):
                python_code += f"{block.name} = {block.value}\n"
            else:
                # Handle other block types as needed
                pass
        return python_code