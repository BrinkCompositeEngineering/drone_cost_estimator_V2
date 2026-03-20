import math

class ToolingStack:

    def __init__(self, thicknesses_available):

        self.max_x = 1500
        self.max_y = 500
        self.thickness_options = sorted(
            [float(t) for t in thicknesses_available]
        )

        self.xy_margin = 100  # total margin

    def calculate_stack(self, product_x, product_y, product_z):

        required_x = product_x + self.xy_margin
        required_y = product_y + self.xy_margin
        required_z = product_z * (4 / 3)

        blocks_x = math.ceil(required_x / self.max_x)
        blocks_y = math.ceil(required_y / self.max_y)

        z_stack = self._calculate_z_stack(required_z)

        leftovers = self._calculate_xy_leftovers(required_x, required_y, z_stack)

        return {
            "required_size": {
                "x": required_x,
                "y": required_y,
                "z": required_z
            },
            "blocks": {
                "x": blocks_x,
                "y": blocks_y,
                "z_layers": z_stack
            },
            "leftovers": leftovers
        }

    def _calculate_xy_leftovers(self, required_x, required_y, z_stack):

        leftovers = []

        used_x = required_x % self.max_x
        used_y = required_y % self.max_y

        if used_x == 0:
            used_x = self.max_x
        if used_y == 0:
            used_y = self.max_y

        for thickness in z_stack:

            # Right-side leftover
            if used_x < self.max_x:
                leftovers.append({
                    "x": self.max_x - used_x,
                    "y": used_y,
                    "z": thickness
                })

            # Top leftover
            if used_y < self.max_y:
                leftovers.append({
                    "x": self.max_x,
                    "y": self.max_y - used_y,
                    "z": thickness
                })

        return leftovers

    def _calculate_z_stack(self, required_z):

        """
        Greedy stacking using largest available thickness.
        """

        remaining = required_z
        stack = []

        for thickness in reversed(self.thickness_options):

            while remaining > thickness:
                stack.append(thickness)
                remaining -= thickness

        # add final block if needed
        if remaining > 0:
            stack.append(min(self.thickness_options))

        return stack