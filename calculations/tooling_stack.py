import math


class ToolingStack:

    def __init__(self, config):

        self.config = config
        self.max_x = self.config.get("tooling_blocks", "standard_block", "length_mm")
        self.max_y = self.config.get("tooling_blocks", "standard_block", "width_mm")

        self.thickness_options = sorted(
            [float(t) for t in self.config.get("tooling_blocks", "standard_block", "thickness_options_mm")]
        )

        self.xy_margin = self.config.get("tooling_blocks", "constraints", "bounding_box_margin_mm")

        self.cut_step = 200  # mm

    # --------------------------------------------------

    def calculate_stack(self, component):
        """
        component: dict with keys {length, width, height}
        """

        # --- STEP 1: Required dimensions ---
        required_x = component.length + self.xy_margin
        required_y = component.width + self.xy_margin
        required_z = component.height * (4 / 3)

        # --- STEP 2: Z stacking ---
        z_stack = self._calculate_z_stack(required_z)

        # --- STEP 3: Y direction (NO cutting allowed) ---
        boards_y = math.ceil(required_y / self.max_y)

        # --- STEP 4: X direction (cutting allowed in 200 mm steps) ---
        full_boards_x = int(required_x // self.max_x)
        remainder_x = required_x % self.max_x

        cut_boards = []
        total_boards_x = full_boards_x

        if remainder_x > 0:
            cut_length = self._round_up_to_step(remainder_x)
            cut_boards.append(cut_length)
            total_boards_x += 1

        # --- STEP 5: Count boards ---
        boards_per_layer = total_boards_x * boards_y
        total_boards = boards_per_layer * len(z_stack)

        # --- STEP 6: Volume calculation ---
        volume = 0
        board_summary = {
            "full_boards": 0,
            "cut_boards": []
        }

        for thickness in z_stack:

            # Full boards
            full_count = full_boards_x * boards_y
            full_volume = full_count * self.max_x * self.max_y * thickness

            volume += full_volume
            board_summary["full_boards"] += full_count

            # Cut boards
            for cut_length in cut_boards:
                cut_count = boards_y
                cut_volume = cut_count * cut_length * self.max_y * thickness

                volume += cut_volume

                board_summary["cut_boards"].append({
                    "count": cut_count,
                    "dimensions": {
                        "x": cut_length,
                        "y": self.max_y,
                        "z": thickness
                    }
                })

        # convert mm³ → m³
        volume_m3 = volume / 1e9

        # --- Populate the component object ---
        component.volume_m3 = volume_m3
        component.z_stack = z_stack
        component.boards_info = {
            "boards_x": total_boards_x,
            "boards_y": boards_y,
            "total_boards": total_boards
        }
        component.required_size = {
            "x": required_x,
            "y": required_y,
            "z": required_z
        }
        component.board_summary = board_summary

        # Flatten all boards for easier downstream use
        all_boards = []
        for thickness in z_stack:
            # Full boards
            for _ in range(full_boards_x * boards_y):
                all_boards.append({"x": self.max_x, "y": self.max_y, "z": thickness})
            # Cut boards
            for cut in board_summary["cut_boards"]:
                for _ in range(cut["count"]):
                    all_boards.append(cut["dimensions"])
        component.all_boards = all_boards

        return component


    # --------------------------------------------------

    def _round_up_to_step(self, value):
        return math.ceil(value / self.cut_step) * self.cut_step

    # --------------------------------------------------

    def _calculate_z_stack(self, required_z):

        remaining = required_z
        stack = []

        for thickness in reversed(self.thickness_options):
            while remaining > thickness:
                stack.append(thickness)
                remaining -= thickness

        if remaining > 0:
            stack.append(min(self.thickness_options))

        return stack


if __name__ == "__main__":

    # --- Mock config class ---
    class MockConfig:
        def __init__(self):
            self.data = {
                "tooling_blocks": {
                    "standard_block": {
                        "length_mm": 1500,
                        "width_mm": 500,
                        "thickness_options_mm": [25, 50, 75,100, 150]
                    },
                    "constraints": {
                        "bounding_box_margin_mm": 100
                    }
                }
            }

        def get(self, *keys):
            value = self.data
            for key in keys:
                value = value[key]
            return value

    # --- Component class ---
    class Component:
        def __init__(self, length, width, height):
            self.length = length
            self.width = width
            self.height = height

    # --- Initialize ---
    config = MockConfig()
    tooling = ToolingStack(config)

    # --- Test component ---
    component = Component(
        length=2100,   # mm
        width=400,    # mm
        height=60      # mm
    )

    # --- Run calculation ---
    # (Make sure your calculate_stack uses component.length etc.)
    result = tooling.calculate_stack(component)

    # --- Print results ---
    print("\n=== TOOLING STACK TEST ===")

    print(result.board_summary)

    # print("\nComponent:")
    # print(f"L={component.length} mm, W={component.width} mm, H={component.height} mm")
    #
    # print("\nRequired Size (mm):")
    # print(result["required_size"])
    #
    # print("\nZ Stack (mm):")
    # print(result["z_stack"])
    #
    # print("\nBoard Usage:")
    # print(result["boards"])
    #
    # print("\nBoard Summary:")
    # print(result["board_summary"])
    #
    # print("\nTotal Volume (m³):")
    # print(round(result["volume_m3"], 4))