from openpyxl import Workbook


class ExcelReport:

    def generate(self, project_name, results, total_cost):

        wb = Workbook()
        ws = wb.active
        ws.title = "Cost Estimate"

        headers = [
            "Component",
            "Mould Length (mm)",
            "Mould Width (mm)",
            "Mould Height (mm)",
            "XY Blocks",
            "Stack Height",
            "Stack Cost",
            "Total Component Cost"
        ]

        ws.append(headers)

        for r in results:

            ws.append([
                r["name"],
                r["mould"]["length"],
                r["mould"]["width"],
                r["mould"]["height"],
                r["xy_blocks"],
                r["stack_height"],
                r["stack_cost"],
                r["component_cost"]
            ])

        ws.append([])
        ws.append(["Total Project Cost", "", "", "", "", "", "", total_cost])

        filename = f"{project_name}_cost_estimate.xlsx"

        wb.save(filename)

        print(f"\nExcel report saved as: {filename}")