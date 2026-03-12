from .component import Component


class Fuselage(Component):

    def __init__(self, length, width, height):
        """
        Fuselage component

        Parameters
        ----------
        length : mm
            Total fuselage length
        width : mm
            Maximum fuselage width
        height : mm
            Maximum fuselage height
        """

        super().__init__("Fuselage", length, width, height)

    def get_dimensions(self):
        return {
            "length": self.length,
            "width": self.width,
            "thickness": self.thickness
        }