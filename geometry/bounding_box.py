class BoundingBox:

    @staticmethod
    def calculate(component):
        dims = component.get_dimensions()

        return {
            "length": dims["length"],
            "width": dims["width"],
            "height": dims["thickness"]
        }