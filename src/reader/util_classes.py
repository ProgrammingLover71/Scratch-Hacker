# This file defines utility classes for representing variables and blocks in a Scratch project.
# These classes are used to store and manipulate data related to Scratch projects.
from typing import Any, Dict


# Variable is a class that represents a variable in a Scratch project.
# It has an ID, a name, a value, and a public flag indicating whether the variable is public or not.
# The ID is a unique identifier for the variable and is a string of 20 alphanumeric characters.
class Variable:
	def __init__(self, id: str, name: str, value: Any, public: bool = False):
		self.id = id
		self.name = name
		self.value = value
		self.public = public 

	def __repr__(self):
		return f"Variable(id='{self.id}', name='{self.name}', value='{self.value}', public={self.public})"
	

# Block is a class that represents a block in a Scratch project.
# It has an ID, an opcode (the type of block), inputs (a dictionary of input values for the block),
# and fields (a dictionary of field values for the block).
class Block:
	def __init__(self, id: str, opcode: str, inputs: Dict[str, Any], fields: Dict[str, Any], next: str = "", parent: str = ""):
		self.id = id
		self.opcode = opcode
		self.inputs = inputs
		self.fields = fields
		self.next = next
		self.parent = parent

	def __repr__(self):
		return f"Block(id='{self.id}', opcode='{self.opcode}', inputs={self.inputs}, fields={self.fields}, next='{self.next}', parent='{self.parent}')"
