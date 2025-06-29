from zipfile import ZipFile
from json import loads
from typing import Any, Dict, List
from util_classes import Variable, Block

# ProjectReader is a class that reads a Scratch project file (.sb3) and extracts variables from it.
# It uses the zipfile module to read the project file and the json module to parse the project's JSON file (named "project.json").
class ProjectReader:
	def __init__(self, project_path: str):
		self.project_path = project_path
		self.project_json = ""
		self.project_asset_files = []
		self.read_project()

	# Read the project and store its data in the the project_json field.
	def read_project(self):
		# Read the project zip file
		with ZipFile(self.project_path, 'r') as zip_file:
			# Read the project's JSON file
			with zip_file.open('project.json') as json_file:
				self.project_json = json_file.read().decode('utf-8')
			# Read the asset files
			self.project_asset_files = [
				file.filename for file in zip_file.infolist()
				if file.filename != 'project.json'
			]

	# Get the list of variables from the project.
	# It returns a list of Variable objects, each representing a variable in the project.
	def get_variables(self) -> List[Variable]:
		if not self.project_json:
			self.read_project()
		
		project_data = loads(self.project_json)
		var_list = []
		# Iterate over all targets in the project
		for target in project_data.get('targets', []):
			# Get the variables from the target
			variables: Dict = target.get('variables', {})
			if variables:
				for variable_id in variables.keys():
					# Get the variable's ID, name, and value and check if it's public
					var_name = variables[variable_id][0]
					var_value = variables[variable_id][1]
					var_public = (var_name in variable_id)
					var_list.append(Variable(
						id=variable_id,
						name=var_name,
						value=var_value,
						public=var_public
					))
		return var_list

	# Get the list of blocks from the project.
	# It returns a list of Block objects, each representing a block in the project.
	def get_blocks(self) -> List[Block]:
		if not self.project_json:
			self.read_project()
		
		project_data = loads(self.project_json)
		block_list = []

		# Iterate over all targets in the project
		for target in project_data.get('targets', []):
			# Get the blocks from the target
			blocks: Dict[str, Any] = target.get('blocks', {})
			if blocks:
				# Iterate over each block in the target
				for block_id in blocks.keys():
					block_data = blocks[block_id]
					# Extract the block's ID, opcode, inputs, and fields
					block_opcode = block_data.get('opcode', '')
					block_inputs = block_data.get('inputs', {})
					block_fields = block_data.get('fields', {})
					block_next = block_data.get('next', None)
					block_parent = block_data.get('parent', None)
					block_list.append(Block(
						id=block_id,
						opcode=block_opcode,
						inputs=block_inputs,
						fields=block_fields,
						next=block_next,
						parent=block_parent
					))
		return block_list
