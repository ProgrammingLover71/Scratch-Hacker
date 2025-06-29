from util_classes import Variable, Block
from typing import List, Tuple

class BlocksToPython:

	# Converts a list of blocks to Python code.
	# This method assumes that the blocks are of type Block for simplicity.
	@staticmethod
	def get_python_from_blocks(blocks: List[Block]) -> str:
		indent = 0
		python_code = ""
		for block in blocks:
			# Convert each block to Python code
			block_code, new_indent = BlocksToPython.convert_block_to_python(block, indent)
			# Append the converted code to the output
			python_code += block_code + "\n"
			# Update the indent level if necessary
			indent = new_indent
		return python_code
	
	# Converts a single block to Python code.
	# This method should be implemented to handle different block types.
	@staticmethod
	def convert_block_to_python(block: Block, indent: int) -> Tuple[str, int]:
		match block.opcode:
			case "data_setvariableto":
				variable_name = block.fields["VARIABLE"][0]
				value = block.inputs["VALUE"][0]
				return f"{' ' * indent}{variable_name} = {value}", indent
			case "data_changevariableby":
				variable_name = block.fields["VARIABLE"][0]
				value = block.inputs["VALUE"][0]
				return f"{' ' * indent}{variable_name} += {value}", indent
			case _:
				# Handle other block types or return a placeholder
				return f"{' ' * indent}# Unsupported block type: {block.opcode}", indent