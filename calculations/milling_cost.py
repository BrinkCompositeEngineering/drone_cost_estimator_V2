def calculate_milling_cost(component, config):
    """
    Calculate milling cost based on removed volume and material-specific MRR.

    Parameters:
        component: Component object with length, width, height, material
        config: ProgramConfig object

    Returns:
        milling_cost (float) in €
        machining_time (float) in hours
    """

    # 1️⃣ Find the selected material properties
    material_name = component.material
    materials = config.get("tooling_blocks", "materials")
    material = next((m for m in materials if m["name"] == material_name), None)

    if material:
        mrr = material["machine_removal_rate"]

    if material is None:
        raise ValueError(f"Material '{material_name}' not found in config.")

    # 2️⃣ Volume to remove (m³)
    # Convert mm -> meters
    block_length_m = component.length / 1000
    block_width_m = component.width / 1000
    block_height_m = component.height / 1000

    # Rough approximation: all material in the block minus final mold volume
    # Here we assume mold_volume is negligible, or you can add actual mold volume
    volume_to_remove_m3 = block_length_m * block_width_m * block_height_m

    # 3️⃣ Material Removal Rate (MRR in m³/h)
    mrr = 0
    if material:
        mrr = material["machine_removal_rate"]
    if mrr is None or mrr <= 0:
        raise ValueError(f"MRR not defined for material '{material_name}'")

    # 4️⃣ Machining time (h)
    machining_time_h = volume_to_remove_m3 / mrr

    # 5️⃣ Machine hourly rate
    machine_rate = config.get("tooling_blocks", "machining", "milling_rate_per_hour")

    # 6️⃣ Milling cost (€)
    milling_cost = machining_time_h * machine_rate

    return milling_cost