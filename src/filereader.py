from .core import Program

def reader(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    
    p = Program(lines)

    p.generate(path)