from geometry.bounding_box import BoundingBox
from mould.mould_generator import MouldGenerator
from mould.block_layout import BlockLayout
from mould.block_library import AVAILABLE_BLOCKS
from mould.block_optimizer import BlockOptimizer
from cost.cost_model import CostModel


class EstimatorEngine:

    def __init__(self):

        self.mould_gen = MouldGenerator(margin=50)
        self.optimizer = BlockOptimizer(AVAILABLE_BLOCKS)
        self.cost_model = CostModel()

    def process_component(self, component):

        bbox = BoundingBox.calculate(component)

        mould = self.mould_gen.generate(bbox)

        layout = BlockLayout.calculate_xy(mould)

        height_solution = self.optimizer.optimize_height(mould["height"])

        cost = self.cost_model.estimate(
            layout["blocks_xy"],
            height_solution
        )

        return {
            "name": component.name,
            "mould": mould,
            "xy_blocks": layout["blocks_xy"],
            "stack_height": height_solution["height"],
            "stack_cost": height_solution["cost"],
            "component_cost": cost["total_cost"]
        }