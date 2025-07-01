from json import dumps
from zipfile import ZipFile

# This module provides functionality to create a Scratch project structure in JSON format.
# It includes methods to create a default stage, add sprites with their blocks and variables,
# and generate the complete project JSON structure.
class ProjectMaker:
    def __init__(self):
        pass


    # Creates a default stage for the Scratch project.
    # The stage includes properties like name, variables, costumes, and sounds.
    def create_default_stage(self):
        return {
            'isStage': True,
            'name': 'Stage',
            'variables': {},
            'lists': {},
            'broadcasts': {},
            'blocks': {},
            'comments': {},
            'currentCostume': 0,
            'costumes': [
                {
                    'name': 'backdrop1',
                    'dataFormat': 'svg',
                    'assetId': 'cd21514d0531fdffb22204e0ec5ed84a',
                    'md5ext': 'cd21514d0531fdffb22204e0ec5ed84a.svg',
                    'rotationCenterX': 240,
                    'rotationCenterY': 180
                }
            ],
            'sounds': [],
            'volume': 100,
            'tempo': 60,
            'layerOrder': 0,
            'videoTransparency': 50,
            'videoState': 'off',
            'textToSpeechLanguage': None,
        }
    

    # Creates a sprite with its blocks and variables.
    # The sprite includes properties like name, variables, costumes, and sounds.
    def create_sprite(self, sprite_blocks, sprite_variables, sprite_name='Sprite'):
        return {
            'isStage': False,
            'name': sprite_name,
            'variables': sprite_variables,
            'lists': {},
            'broadcasts': {},
            'blocks': sprite_blocks,
            'comments': {},
            'currentCostume': 0,
            'costumes': [
                {
                    'name': 'costume1',
                    'dataFormat': 'svg',
                    'assetId': 'bcf454acf82e4504149f7ffe07081dbc',
                    'md5ext': 'bcf454acf82e4504149f7ffe07081dbc.svg',
                    'rotationCenterX': 50,
                    'rotationCenterY': 50
                }
            ],
            'sounds': [],
            'layerOrder': 1,
            'x': 0,
            'y': 0,
            'direction': 90,
            'size': 100,
            'visible': True,
            'draggable': False,
            'rotationStyle': 'all around',
        }


    # Creates the complete Scratch project JSON structure.
    # It includes the default stage and a sprite with its blocks and variables.
    def create_project_json(self, sprite_data: dict):
        return {
            'targets': [
                self.create_default_stage(),
                self.create_sprite(sprite_data['blocks'], sprite_data['variables'], sprite_data['name'])
            ],
            'monitors': [],
            'extensions': [],
            'meta': {
                'semver': '3.0.0',
                'vm': '2.0.0',
                'agent': 'PythonToBlocks Compiler v1.0 (Scratch Hacker)',
                'isScratch3Project': True
            }
        }
    
    # Saves the project JSON to a file and creates a ZIP archive.
    def save_project(self, project_json, filename='project.sb3'):
        with ZipFile(filename, 'w') as zip_file:
            # Save the project JSON to a file inside the ZIP archive
            zip_file.writestr('project.json', dumps(project_json, indent=4))
            # Add the assets (costumes) to the ZIP archive
            zip_file.write('./transpilers/project_assets/cd21514d0531fdffb22204e0ec5ed84a.svg', 'cd21514d0531fdffb22204e0ec5ed84a.svg')
            zip_file.write('./transpilers/project_assets/bcf454acf82e4504149f7ffe07081dbc.svg', 'bcf454acf82e4504149f7ffe07081dbc.svg')
        