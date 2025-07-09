from reader.project_reader import ProjectReader
from transpilers.blocks_to_python import BlocksToPython
from transpilers.python_to_blocks import PythonToBlocks

def main():
    print("Scratch Hacker v1.0-beta-1. (Shell version)\nCopyright (c) 2025 ProgrammingLover71.\n")
    while True:
        proj = input("SH -- Enter project to read >>   ") + '.sb3'
        try:
            pr = ProjectReader(proj)
            blocks = pr.get_blocks()
            vars = pr.get_variables()
            b2p = BlocksToPython()
            print(f"Project code (displaying as Python):\n{'=' * 32}")
            # Load all targets
            targets = set()
            for block in blocks:
                targets.add(block.target)
            
            for target in targets:
                print(f"\n###====== TARGET: \"{target}\" ======###")
                print(b2p.get_python_from_blocks(blk for blk in blocks if blk.target == target))
        except FileNotFoundError as f:
            print(f"Project file could not be found: {proj} ({f.strerror})")