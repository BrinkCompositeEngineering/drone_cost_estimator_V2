def calculate_milling_cost(component, config):

    rate = config.get("machining", "machine_hour_rate")
    roughing_factor = config.get("machining", "roughing_factor")

    surface_area = (
        component.length * component.width
    ) / 1_000_000

    hours = surface_area * roughing_factor

    return hours * rate