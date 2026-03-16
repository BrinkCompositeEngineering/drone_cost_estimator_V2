class BlockOptimizer:

    def __init__(self, config):

        self.block_length = config.get("blocks", "block_length")
        self.block_width = config.get("blocks", "block_width")

        # leftover pieces from previous cuts
        self.leftover_lengths = []

        self.total_blocks_used = 0


    def _use_leftover(self, required_length):

        for i, leftover in enumerate(self.leftover_lengths):

            if leftover >= required_length:

                new_leftover = leftover - required_length

                self.leftover_lengths.pop(i)

                if new_leftover > 0:
                    self.leftover_lengths.append(new_leftover)

                return True

        return False


    def allocate_length(self, required_length):

        # Try using leftover stock first
        if self._use_leftover(required_length):
            return "used_leftover"


        # Otherwise use a new block
        self.total_blocks_used += 1

        leftover = self.block_length - required_length

        if leftover > 0:
            self.leftover_lengths.append(leftover)

        return "new_block"


    def process_component(self, component):

        required_length = component.length

        blocks_needed = 0

        remaining = required_length

        while remaining > 0:

            piece = min(self.block_length, remaining)

            result = self.allocate_length(piece)

            if result == "new_block":
                blocks_needed += 1

            remaining -= piece

        return blocks_needed

def calculate_block_stack(height, available_thickness):

    available_thickness = sorted(available_thickness, reverse=True)

    stack = []

    remaining = height

    for t in available_thickness:

        while remaining >= t:
            stack.append(t)

            remaining -= t

    if remaining > 0:
        stack.append(min(available_thickness))

    return stack