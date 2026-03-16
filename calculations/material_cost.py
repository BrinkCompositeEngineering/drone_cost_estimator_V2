def calculate_material_cost(component, config):

    volume_m3 = (
        component.length
        * component.width
        * component.height
    ) / 1_000_000_000



    cost = volume_m3 * config.get("block_cost", component.material)

    return cost