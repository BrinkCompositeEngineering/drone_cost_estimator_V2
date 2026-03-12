class BlockType:

    def __init__(self, thickness, price):
        self.thickness = thickness
        self.price = price


AVAILABLE_BLOCKS = [
    BlockType(25, 300),
    BlockType(50, 400),
    BlockType(75, 500),
    BlockType(100, 600),
    BlockType(150, 900),
]