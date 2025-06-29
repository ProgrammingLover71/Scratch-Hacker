from util_classes import Variable, Block
from typing import List

class BlocksToPython:

	# Converts a list of blocks to Python code.
	# This method assumes that the blocks are of type Block for simplicity.
	@staticmethod
	def get_python_from_blocks(blocks: List[Block]) -> str:
		indent = 0
		python_code = ""
		for block in blocks:
			# Match the block's opcode and convert it to Python code
			match block.opcode:
				case "motion_movesteps":
					input_type = block.inputs['STEPS'][0]
					expr = None
					if input_type == 1:
						expr = block.inputs['STEPS'][1][1]
					python_code += "\t" * indent + f"move({expr})\n"
				case "event_whenflagclicked":
					python_code += "if flag_clicked():\n"
					indent += 1
				
		return python_code