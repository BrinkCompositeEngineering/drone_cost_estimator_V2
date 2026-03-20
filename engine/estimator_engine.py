from calculations.material_cost import calculate_material_cost
from calculations.milling_cost import calculate_milling_cost
from calculations.postprocess_cost import calculate_postprocess_cost
from calculations.block_optimizer import BlockOptimizer
from calculations.block_optimizer import calculate_block_stack
from calculations.tooling_stack import ToolingStack


class EstimatorEngine:

    def __init__(self, config_default, config_tooling):

        self.config_default = config_default
        self.config_tooling = config_tooling
        self.block_optimizer = BlockOptimizer(config_default)

        # board_names = list(self.config_tooling.data["raku_tool_tooling_boards"].keys())
        #
        # print(board_names)


    def process_component(self, component):

        # Using the Tooling_stack module
        stacker = ToolingStack(self.config_default.get("tooling_blocks","standard_block", "thickness_options_mm"))

        result = stacker.calculate_stack(
            product_x=component.length,
            product_y=component.width,
            product_z=component.height
        )

        print("Component.material: " + component.material)


        material = calculate_material_cost(component, self.config_default)

        milling = calculate_milling_cost(component, self.config_default)

        post = calculate_postprocess_cost(component, self.config_default)

        thickness_options = self.config_default.get(
            "tooling_blocks", "standard_block", "thickness_options_mm"
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