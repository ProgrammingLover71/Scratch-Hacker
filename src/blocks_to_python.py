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
		match block.opcode:
			###### EVENT BLOCKS ######
			case "event_whenflagclicked":
				inner_block_id = block.next
				blocks = []
				loop_block = Block("", "", {}, {})
				# Traverse the inner block to find all blocks
				while inner_block_id != None:		
					loop_block = self.get_block_by_id(inner_block_id)
					blocks.append(loop_block)
					inner_block_id = loop_block.next
				# Convert the inner blocks to Python code
				inner_code = ""
				for inner_block in blocks:
					inner_block_code, _ = self.convert_block_to_python(inner_block, indent)
					if inner_block_code:
						inner_code += f"{' ' * (indent + 4)}{inner_block_code.strip()}\n"
				return f"{' ' * indent}@when_flag_clicked\n{' ' * indent}def main():\n{inner_code}", indent
			
			###### DATA BLOCKS ######
			case "data_setvariableto":
				variable_name = block.fields["VARIABLE"][0]
				value = self.parse_input(block.inputs["VALUE"])
				return f"{' ' * indent}{variable_name} = {value}", indent
			
			case "data_changevariableby":
				variable_name = block.fields["VARIABLE"][0]
				value = self.parse_input(block.inputs["VALUE"])
				return f"{' ' * indent}{variable_name} += {value}", indent
			
			###### OPERATOR BLOCKS ######
			case "operator_add":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} + {right_value})", indent
			
			case "operator_subtract":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} - {right_value})", indent

			case "operator_multiply":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} * {right_value})", indent
			
			case "operator_divide":
				left_value = self.parse_input(block.inputs["NUM1"])
				right_value = self.parse_input(block.inputs["NUM2"])
				return f"({left_value} / {right_value})", indent
			
			case "operator_random":
				min_value = self.parse_input(block.inputs["FROM"])
				max_value = self.parse_input(block.inputs["TO"])
				return f"random_int({min_value}, {max_value})", indent
			
			case "operator_gt":
				left_value = self.parse_input(block.inputs["OPERAND1"])
				right_value = self.parse_input(block.inputs["OPERAND2"])
				return f"({left_value} > {right_value})", indent
			
			###### MOTION BLOCKS ######
			case "motion_movesteps":
				steps = self.parse_input(block.inputs["STEPS"])
				return f"{' ' * indent}move_steps({steps})", indent
			
			case "motion_turnright":
				steps = self.parse_input(block.inputs["DEGREES"])
				return f"{' ' * indent}turn_degrees({steps})", indent
			
			case "motion_turnleft":
				steps = self.parse_input(block.inputs["DEGREES"])
				return f"{' ' * indent}turn_degrees(-{steps})", indent
			
			case "motion_direction":
				return f"{' ' * indent}direction", indent
			
			###### LOOKS BLOCKS ######
			case "looks_say":
				message = self.parse_input(block.inputs["MESSAGE"])
				return f"{' ' * indent}say({message})", indent
			
			case "looks_sayforsecs":
				message = self.parse_input(block.inputs["MESSAGE"])
				seconds = self.parse_input(block.inputs["SECS"])
				return f"{' ' * indent}say_for_secs({message}, {seconds})", indent
			
			###### CONTROL BLOCKS ######
			case "control_forever":
				inner_block_id = block.inputs["SUBSTACK"][1]
				blocks = []
				loop_block = Block("", "", {}, {})
				# Traverse the inner block to find all blocks
				while inner_block_id != None:
					loop_block = self.get_block_by_id(inner_block_id)
					blocks.append(loop_block)
					inner_block_id = loop_block.next
				# Convert the inner blocks to Python code
				inner_code = ""
				for inner_block in blocks:
					inner_block_code, _ = self.convert_block_to_python(inner_block, indent + 4)
					if inner_block_code:
						inner_code += f"{' ' * (indent + 4)}{inner_block_code}\n"
				return f"{' ' * indent}while True:\n{inner_code}", indent

			case "control_if":
				condition = self.parse_input(block.inputs["CONDITION"])
				inner_block_id = block.inputs["SUBSTACK"][1]
				blocks = []
				loop_block = Block("", "", {}, {})
				# Traverse the inner block to find all blocks
				while inner_block_id != None:
					loop_block = self.get_block_by_id(inner_block_id)
					blocks.append(loop_block)
					inner_block_id = loop_block.next
				# Convert the inner blocks to Python code
				inner_code = ""
				for inner_block in blocks:
					inner_block_code, _ = self.convert_block_to_python(inner_block, indent + 2)
					if inner_block_code:
						inner_code += f"{' ' * (indent + 2)}{inner_block_code}\n"
				return f"{' ' * indent}if {condition}:\n{inner_code}", indent

			case _:
				# Handle other block types or return a placeholder
				return f"\'{block.opcode}\'", indent
	
	# Parses the input of a block and returns a Python-compatible value.
	def parse_input(self, input_data: List[Any]) -> Any:
		if not input_data:
			return "None"
		
		value_type = input_data[0]
		value_data = input_data[1:]  # Remove the type from the input data

		# In-place value (literal)
		if value_type == 1:
			try:
				return float(value_data[-1][1])
			except ValueError:
				return f"\"{value_data[-1][1]}\""
		
		# Block or Variable (nested input)
		elif value_type == 2 or value_type == 3:
			data = value_data[0]
			
			if isinstance(data, list):  # Variable reference
				var_name = data[1]
				return var_name
			
			else:  # Block ID
				block_id = data
				for block in self.blocks:
					if block.id == block_id:
						# Check if it's an expression block
						if self.is_expression_block(block.opcode):
							block_code, _ = self.convert_block_to_python(block, 0)
							return block_code.strip()
						else:
							# Unsupported statement in expression context
							return "None"
		
		return "None"  # Fallback

	
	# Retrieves a block based on its ID
	def get_block_by_id(self, id: str) -> Block:
		for block in self.blocks:
				if block.id == id:
					return block
		return Block("", "", {}, {})  # Return an empty block if not found
	
	def is_expression_block(self, opcode: str) -> bool:
		return opcode.startswith("operator_") or opcode.startswith("sensing_") or opcode.startswith("data_") or opcode in [
			"motion_direction", "motion_xposition", "motion_yposition"
		]
 