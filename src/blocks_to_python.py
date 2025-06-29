from util_classes import Variable, Block
from typing import Any, List, Tuple

class BlocksToPython:
	def __init__(self):
		self.blocks = []

	# Converts a list of blocks to Python code.
	# This method assumes that the blocks are of type Block for simplicity.
	def get_python_from_blocks(self, blocks: List[Block]) -> str:
		indent = 0
		python_code = "from scratch_hacker import *\n\n"
		self.blocks = blocks   # Store the blocks for potential use as arguments in other blocks
		for block in blocks:
			# Convert each block to Python code
			block_code, new_indent = self.convert_block_to_python(block, indent)
			# If the block code is empty, skip it
			if not block_code:
				continue
			# Append the converted code to the output
			python_code += block_code + "\n"
			# Update the indent level if necessary
			indent = new_indent
		
		# Add code to call the main function
		python_code += "\nif __name__ == '__main__':\n\tmain()\n\texit(0)\n"
		return python_code
	
	# Converts a single block to Python code.
	# This method should be implemented to handle different block types.
	def convert_block_to_python(self, block: Block, indent: int) -> Tuple[str, int]:
		if block.was_parsed:
			return "", indent  # If the block was already parsed, return an empty string and the current indent level
		block.was_parsed = True  # Mark the block as parsed to avoid re-parsing it
		#print(f"Parsing block: {block.opcode} with ID: {block.id}")
		match block.opcode:
			case "event_whenflagclicked":
				# Handle the "when flag clicked" block
				return f"{' ' * indent}def main():", indent + 4
			
			case "data_setvariableto":
				variable_name = block.fields["VARIABLE"][0]
				value = self.parse_input(block.inputs["VALUE"])
				return f"{' ' * indent}{variable_name} = {value}", indent
			
			case "data_changevariableby":
				variable_name = block.fields["VARIABLE"][0]
				value = self.parse_input(block.inputs["VALUE"])
				return f"{' ' * indent}{variable_name} += {value}", indent
			
			case "operator_add":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} + {right_value})", indent
			
			case "operator_subtract":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} - {right_value})", indent
			
			case "motion_movesteps":
				steps = self.parse_input(block.inputs["STEPS"])
				return f"{' ' * indent}move_steps({steps})", indent
			
			case _:
				# Handle other block types or return a placeholder
				return f"\'{block.opcode}\'", indent
	
	# Parses the input of a block and returns a Python-compatible value.
	def parse_input(self, input_data: List[Any]) -> Any:
		value_type = input_data[0]
		value_data = input_data[1:]  # Remove the type from the input data
		
		# In-place value
		if value_type == 1:
			return value_data[-1][1]
		
		# Block/Variable as value
		elif value_type == 3:
			# Handle blocks as inputs
			data = value_data[0]
			if isinstance(data, list):   # If the data is a list, then we have a variable
				var_name = data[1]
				return f"{var_name}"
			else:   # Otherwise, we have a block ID
				block_id = data
				# Find the block with the given ID in the stored blocks
				for block in self.blocks:
					if block.id == block_id:
						block_code, _ = self.convert_block_to_python(block, 0)
						return block_code.strip()
