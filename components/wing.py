from .component import Component

class Wing(Component):
    def __init__(self, span, chord, thickness):
        super().__init__("Wing", span, chord, thickness)