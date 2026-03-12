import math

class BlockOptimizer:

    def __init__(self, block_types):
        self.block_types = block_types

    def optimize_height(self, required_height):

        max_height = required_height + 150

        dp = [float("inf")] * (max_height + 1)
        choice = [None] * (max_height + 1)

        dp[0] = 0

        for h in range(max_height + 1):
            for block in self.block_types:

                next_h = h + block.thickness

                if next_h <= max_height:

                    cost = dp[h] + block.price

                    if cost < dp[next_h]:
                        dp[next_h] = cost
                        choice[next_h] = block

        best_height = None
        best_cost = float("inf")

        for h in range(required_height, max_height + 1):
            if dp[h] < best_cost:
                best_cost = dp[h]
                best_height = h

        stack = []
        h = best_height

        while h > 0:
            block = choice[h]
            stack.append(block)
            h -= block.thickness

        return {
            "height": best_height,
            "cost": best_cost,
            "stack": stack
        }