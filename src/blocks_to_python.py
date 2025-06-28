from util_classes import Variable, Block
from typing import List

class BlocksToPython:

    # Converts a list of blocks to Python code.
    # This method assumes that the blocks are of type Block for simplicity.
    @staticmethod
    def get_python_from_blocks(blocks: List[Block]) -> str:
        python_code = ""
        for block in blocks:
            # Match the block's opcode and convert it to Python code
            match block.opcode:
                case "motion_movesteps":
                    python_code += f"move({block.inputs['STEPS'][1][-1]})\n"
        return python_code