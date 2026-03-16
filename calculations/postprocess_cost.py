def calculate_postprocess_cost(component, config):

    base_cost = 50

    size_factor = (
        component.length
        * component.width
    ) / 1_000_000

    return base_cost + size_factor * 30