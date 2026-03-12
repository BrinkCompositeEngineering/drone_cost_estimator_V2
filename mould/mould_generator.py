class MouldGenerator:

    def __init__(self, margin=50):
        self.margin = margin

    def generate(self, bounding_box):

        mould = {
            "length": bounding_box["length"] + 2 * self.margin,
            "width": bounding_box["width"] + 2 * self.margin,
            "height": bounding_box["height"] + self.margin
        }

        return mould