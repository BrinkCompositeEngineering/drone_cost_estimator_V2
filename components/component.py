class Component:
    def __init__(self, name, length, width, thickness):
        self.name = name
        self.length = length
        self.width = width
        self.thickness = thickness

    def get_dimensions(self):
        return {
            "length": self.length,
            "width": self.width,
            "thickness": self.thickness
        }