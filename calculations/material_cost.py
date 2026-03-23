def calculate_material_cost(component, config):

    volume_m3 = (
        component.length
        * component.width
        * component.height
    ) / 1_000_000_000

    materials = config.get("tooling_blocks", "materials")

    selected_name = component.material

    material = next((m for m in materials if m["name"] == selected_name), None)

    if material:
        price = material["price_per_m3"]


    cost = volume_m3 * price

    return cost