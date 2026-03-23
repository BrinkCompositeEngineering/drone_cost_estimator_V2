class ReportGenerator:

    def __init__(self, components):
        self.components = components

    # -----------------------------
    def generate_summary(self):

        total_cost = 0
        total_volume = 0
        total_boards = 0

        for comp in self.components:
            total_cost += comp.total_cost
            total_volume += comp.volume_m3
            total_boards += comp.boards_info["total_boards"]

        return {
            "total_cost": total_cost,
            "total_volume": total_volume,
            "total_boards": total_boards,
            "num_components": len(self.components)
        }

    # -----------------------------
    def generate_component_table(self):

        rows = []

        for comp in self.components:
            rows.append({
                "Component": comp.name,
                "Volume (m3)": round(comp.volume_m3, 4),
                "Material Cost (€)": round(comp.material_cost, 2),
                "Milling Cost (€)": round(comp.milling_cost, 2),
                "Total (€)": round(comp.total_cost, 2),
                "Boards": comp.boards_info["total_boards"]
            })

        return rows