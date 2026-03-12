from components.wing import Wing
from components.component import Component
from components.fuselage import Fuselage
from geometry.bounding_box import BoundingBox
from mould.mould_generator import MouldGenerator
from mould.block_layout import BlockLayout
from mould.block_library import AVAILABLE_BLOCKS
from mould.block_optimizer import BlockOptimizer
from cost.cost_model import CostModel
from project.project import Project
from report.excel_report import ExcelReport


def process_component(component, mould_gen, optimizer, cost_model):

    bbox = BoundingBox.calculate(component)
    mould = mould_gen.generate(bbox)

    layout = BlockLayout.calculate_xy(mould)

    height_solution = optimizer.optimize_height(mould["height"])

    cost = cost_model.estimate(
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


def main():

    # -------------------------------------------------
    # Initialize systems
    # -------------------------------------------------

    mould_gen = MouldGenerator(margin=50)
    optimizer = BlockOptimizer(AVAILABLE_BLOCKS)
    cost_model = CostModel()

    # -------------------------------------------------
    # Create project
    # -------------------------------------------------

    drone_project = Project("Drone1")

    # Add components
    drone_project.add_component(Wing(span=3200, chord=400, thickness=60))
    drone_project.add_component(Wing(span=3200, chord=400, thickness=60))  # second wing
    drone_project.add_component(Component("Winglet", 300, 150, 40))
    drone_project.add_component(Component("Elevator", 600, 200, 35))
    drone_project.add_component(Component("Rudder", 500, 220, 40))
    drone_project.add_component(Fuselage(length=1800, width=250, height=300))

    # -------------------------------------------------
    # Process components
    # -------------------------------------------------

    results = []
    total_cost = 0

    for component in drone_project.get_components():
        result = process_component(
            component,
            mould_gen,
            optimizer,
            cost_model
        )

        results.append(result)

        total_cost += result["component_cost"]

    # -------------------------------------------------
    # Final project cost
    # -------------------------------------------------

    print("\n=================================")
    print("PROJECT:", drone_project.name)
    print("Total tooling cost estimate:", total_cost)
    print("=================================")

    report = ExcelReport()
    report.generate(
        drone_project.name,
        results,
        total_cost
    )


if __name__ == "__main__":
    main()