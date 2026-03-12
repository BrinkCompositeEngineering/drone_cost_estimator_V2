import math

class BlockLayout:

    BLOCK_LENGTH = 1500
    BLOCK_WIDTH = 500

    @staticmethod
    def calculate_xy(mould):

        n_length = math.ceil(mould["length"] / BlockLayout.BLOCK_LENGTH)
        n_width = math.ceil(mould["width"] / BlockLayout.BLOCK_WIDTH)

        return {
            "blocks_length": n_length,
            "blocks_width": n_width,
            "blocks_xy": n_length * n_width
        }