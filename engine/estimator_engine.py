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


    def process_component(self, component):

        # Using the Tooling_stack module input the
        stacker = ToolingStack(self.config_default)

        stackerResult = stacker.calculate_stack(component)

        materialcost = calculate_material_cost(component,self.config_default)

        millingcost = calculate_milling_cost(component,self.config_default)

        component.stacker_result = stackerResult
        component.material_cost = materialcost
        component.milling_cost = millingcost




        return component