from calculations.material_cost import calculate_material_cost
from calculations.milling_cost import calculate_milling_cost
from calculations.postprocess_cost import calculate_postprocess_cost
from calculations.block_optimizer import BlockOptimizer
from calculations.block_optimizer import calculate_block_stack


class EstimatorEngine:

    def __init__(self, config):

        self.config = config
        self.block_optimizer = BlockOptimizer(config)


    def process_component(self, component):

        material = calculate_material_cost(component, self.config)

        milling = calculate_milling_cost(component, self.config)

        post = calculate_postprocess_cost(component, self.config)

        thickness_options = self.config.get(
            "blocks", "available_thickness"
        )

        stack = calculate_block_stack(
            component.height,
            thickness_options
        )

        blocks = self.block_optimizer.process_component(component)

        return {
            "material_cost": material,
            "milling_cost": milling,
            "postprocess_cost": post,
            "total_cost": material + milling + post,
            "block_stack": stack,
            "blocks_used": blocks,
            "leftover_stock": self.block_optimizer.leftover_lengths
        }