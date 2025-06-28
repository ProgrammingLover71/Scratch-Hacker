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
                    input_type = block.inputs['STEPS'][0]
                    expr = None
                    if input_type == 1:
                        expr = block.inputs['STEPS'][1][1]
                    python_code += f"move({expr})\n"
        return python_code