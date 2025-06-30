class ProjectMaker:
    def __init__(self):
        pass

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


    def create_project_json(self, sprite_data: list):
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
                'agent': 'PythonToScratch Compiler v1.0',
                'isScratch3Project': True
            }
        }