class CostModel:

    def estimate(self, xy_blocks, height_solution):

        stack_cost = height_solution["cost"]

        total_cost = xy_blocks * stack_cost

        return {
            "cost_per_stack": stack_cost,
            "xy_blocks": xy_blocks,
            "total_cost": total_cost
        }