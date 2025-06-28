from zipfile import ZipFile
from json import loads
from typing import Any, Dict, List


# Variable is a class that represents a variable in a Scratch project.
# It has an ID, a name, a value, and a public flag indicating whether the variable is public or not.
# The ID is a unique identifier for the variable and is a string of 20 alphanumeric characters.
class Variable:
    def __init__(self, id: str, name: str, value: Any, public: bool):
        self.id = id
        self.name = name
        self.value = value
        self.public = public

    def __repr__(self):
        return f"Variable(id={self.id}, name={self.name}, value={self.value}, public={self.public})"


# ProjectReader is a class that reads a Scratch project file (.sb3) and extracts variables from it.
# It uses the zipfile module to read the project file and the json module to parse the project's JSON file (named "project.json").

class ProjectReader:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.project_json = None
        self.project_asset_files = []
        self.read_project()

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
    
    def get_variables(self) -> List[Variable]:
        if not self.project_json:
            raise ValueError("Project JSON not loaded.")
        
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
