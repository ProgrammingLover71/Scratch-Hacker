from typing import Any

# Variable class
class Variable:
    def __init__(self, name: str, value: Any, target: str = "", id: str = "", public: bool = False):
        self.name = name
        self.value = value
        self.target = target
        self.id = id
        self.public = public
    
    def __repr__(self):
        return f"Variable(name={self.name}, value={self.value}, target={self.target}; id={self.id} public={self.public})"
    